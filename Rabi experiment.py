import numpy as np
from qiskit.ignis.characterization.calibrations import rabi_schedules, RabiFitter

from qiskit.pulse import DriveChannel
from qiskit.compiler import assemble
#from qiskit.qobj.utils import MeasLevel, MeasReturnType
# The pulse simulator
from qiskit.providers.aer import PulseSimulator

# Object for representing physical models
from qiskit.providers.aer.pulse import PulseSystemModel

# Mock Armonk backend
from qiskit.test.mock.backends.armonk.fake_armonk import FakeArmonk
armonk_backend = FakeArmonk()
freq_est = 4.97e9
drive_est = 6.35e7
armonk_backend.defaults().qubit_freq_est = [freq_est]
armonk_backend.configuration().hamiltonian['h_str']= ['wq0*0.5*(I0-Z0)', 'omegad0*X0||D0']
armonk_backend.configuration().hamiltonian['vars'] = {'wq0': 2 * np.pi * freq_est, 'omegad0': drive_est}
armonk_backend.configuration().hamiltonian['qub'] = {'0': 2}
armonk_backend.configuration().dt = 2.2222222222222221e-10
armonk_model = PulseSystemModel.from_backend(armonk_backend)
# qubit list
qubits = [0]

# drive amplitudes to use
num_exps = 64
drive_amps = np.linspace(0, 1.0, num_exps)

# drive shape parameters
drive_duration = 2048
drive_sigma = 256

# list of drive channels
drive_channels = [DriveChannel(0)]

# construct the schedules
rabi_schedules, xdata = rabi_schedules(amp_list=drive_amps,
                                       qubits=qubits,
                                       pulse_width=drive_duration,
                                       pulse_sigma=drive_sigma,
                                       drives=drive_channels,
                                       inst_map=armonk_backend.defaults().instruction_schedule_map,
                                       meas_map=armonk_backend.configuration().meas_map)
backend_sim = PulseSimulator()

rabi_qobj = assemble(rabi_schedules,
                     backend=backend_sim,
                     meas_level=1,
                     meas_return='avg',
                     shots=512)
sim_result = backend_sim.run(rabi_qobj, system_model=armonk_model).result()
rabi_fit = RabiFitter(sim_result, xdata, qubits, fit_p0 = [1.5, 2, 0, 0])

# get the pi amplitude
pi_amp = rabi_fit.pi_amplitude(0)

# plot
rabi_fit.plot(0)
print('Pi Amp: %f'%pi_amp)
