from qiskit import IBMQ, pulse, assemble
from qiskit.pulse import DriveChannel, Play, Schedule
from qiskit.pulse.library import Gaussian

import numpy as np

# make the styles nice for dark background
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from qiskit.visualization.pulse_v2.stylesheet import IQXDebugging
style = IQXDebugging()
style.update({"formatter.color.axis_label": "#ffffff",
              "formatter.color.fig_title": "#ffffff", 
              "formatter.general.fig_width": 20,
              "formatter.text_size.fig_title": 20,
              "formatter.control.show_acquire_channel": False})

from qiskit import IBMQ
IBMQ.save_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend=provider.get_backend('ibmq_armonk')
backend_config = backend.configuration()
assert backend_config.open_pulse, "Backend doesn't support Pulse"
dt = backend_config.dt
print(f"Sampling time: {dt*1e9} ns")    # The configuration returns dt in seconds, so multiply by
                                        # 1e9 to get nanoseconds
backend_defaults = backend.defaults()
import numpy as np

qubit = 0 # it's the only one

# unit conversion factors -> all backend properties returned in SI (Hz, sec, etc.)
GHz = 1.0e9 # Gigahertz
MHz = 1.0e6 # Megahertz
us = 1.0e-6 # Microseconds
ns = 1.0e-9 # Nanoseconds

# scale factor to remove factors of 10 from the data
scale_factor = 1e-14
num_shots = 1024

center_frequency_Hz = backend.defaults().qubit_freq_est[qubit] # qubit frequency given in Hz
                                                                    
print(f"Qubit {qubit} has an estimated frequency of %.3f GHz." % (center_frequency_Hz / GHz))

# sweep 100 MHz around the estimated frequency in steps of 2 MHz
frequency_span_Hz = 100 * MHz
frequency_step_Hz = 2 * MHz
frequency_min = center_frequency_Hz - frequency_span_Hz / 2
frequency_max = center_frequency_Hz + frequency_span_Hz / 2
frequencies_GHz = np.arange(frequency_min / GHz, 
                            frequency_max / GHz, 
                            frequency_step_Hz / GHz)

print(f"The sweep will go from %.3f GHz to %.3f GHz \
in steps of %.1f MHz." % ((frequency_min / GHz), (frequency_max / GHz), (frequency_step_Hz / MHz)))  



inst_sched_map_arm = backend.defaults().instruction_schedule_map

x_arm = inst_sched_map_arm.get('x', qubits=[qubit])
meas_arm = inst_sched_map_arm.get('measure', qubits=[qubit])
x_arm.instructions

# create the single base schedule
schedule = Schedule(name='Frequency sweep')
schedule |= x_arm
schedule |= meas_arm << schedule.duration

schedule.draw(style=style)

# define frequencies for the sweep
freqs = frequencies_GHz*GHz
schedule_freqs = [{DriveChannel(qubit): freq} for freq in freqs]

# assemble the program in to a QObj (deprecated)
# this constructs the same schedule, but with an array of LO frequencies for the sweep
freq_sweep_arm = assemble(schedule,
                             backend=backend, 
                             meas_level=1,
                             meas_return='avg',
                             shots=num_shots,
                             schedule_los=schedule_freqs)

freq_offsets = np.linspace(-frequency_span_Hz/2, frequency_span_Hz/2, int(frequency_span_Hz/frequency_step_Hz)+1)
schedules = []
for freq_off in freq_offsets:
    with pulse.build() as sched:
        with pulse.align_sequential():
            with pulse.frequency_offset(freq_off, DriveChannel(qubit)):
                pulse.call(x_arm)
            pulse.call(meas_arm)
            
    schedules.append(sched)
    
schedules[-1].draw(style=style)


from scipy.optimize import curve_fit

def fit_function(x_values, y_values, function, init_params):
    """Fit a function using scipy curve_fit."""
    fitparams, conv = curve_fit(function, x_values, y_values, init_params)
    y_fit = function(x_values, *fitparams)
    
    return fitparams, y_fit

def lorentzian(x, A, q_freq, B, C): 
    return (A / np.pi) * (B / ((x - q_freq)**2 + B**2)) + C

inst_sched_map_arm = backend.defaults().instruction_schedule_map
backend.configuration().open_pulse
x_arm = inst_sched_map_arm.get('x', qubits=[qubit])
x_arm.instructions

from qiskit.circuit import Gate, QuantumCircuit
spec_circ = QuantumCircuit(1, 1)
spec_circ.x(0)
spec_circ.measure(0, 0)
spec_circ.draw(output='mpl')

from copy import deepcopy

spec_circs = []
for freq_off in freq_offsets:
    spec_circ_off = deepcopy(spec_circ)
    with pulse.build() as sched:
        with pulse.frequency_offset(freq_off, DriveChannel(qubit)):
            pulse.call(x_arm)
        
        spec_circ_off.add_calibration('x', [qubit], sched)
            
    spec_circs.append(spec_circ_off)
    
job_arm = backend.run(spec_circs, meas_level=1, meas_return='avg', shots=num_shots)
from qiskit.tools.monitor import job_monitor
job_monitor(job_arm)

job_results = job_arm.result() 
result_data = []
for idx in range(len(job_results.results)):
    result_data.append(job_results.get_memory(idx)[qubit]*scale_factor) 
    
sweep_data3 = np.real(result_data)

# do fit in Hz
freqs3 = backend.properties().frequency(qubit) - freq_offsets

(sweep_fit_params3, sweep_y_fit3) = fit_function(freqs3,
                                   sweep_data3, 
                                   lorentzian,
                                   [7, 4.97*GHz, 0.1*GHz, 3*GHz] # initial parameters for curve_fit
                                   )

plt.scatter(freqs3/GHz, sweep_data3, color='white')
plt.plot(freqs3/GHz, sweep_y_fit3, color='red')
plt.xlim([min(freqs3/GHz), max(freqs3/GHz)])
plt.xlabel("Frequency [GHz]", fontsize=15)
plt.ylabel("Measured Signal [a.u.]", fontsize=15)
plt.title("Armonk: 0->1 Frequency Sweep", fontsize=15)
print("Measured qubit frequency is %.3f GHz" % (sweep_fit_params3[1]/GHz))
plt.show()

