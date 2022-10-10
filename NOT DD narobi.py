from qiskit import pulse
from qiskit.pulse import Acquire, AcquireChannel, MemorySlot, ControlChannel, DriveChannel
from qiskit import IBMQ
from qiskit import schedule, transpile, execute
from qiskit.tools.monitor import job_monitor
from qiskit.circuit import Gate
from numpy import *
import warnings
from qiskit.visualization import plot_state_city, plot_bloch_multivector, plot_histogram
from qiskit.tools.visualization import plot_histogram,plot_state_city, plot_bloch_vector,plot_state_qsphere
warnings.filterwarnings('ignore')


channel = DriveChannel(0)

IBMQ.save_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend=provider.get_backend('ibm_nairobi')

from qiskit.pulse import library

amp = (0.13964000768620577+0j)#Narobi Pi amplitude
amp90 = 0.06989063434283332+2.8058840562449595e-05j #narobi pi/2 amplitude
sigma = 40
num_samples = 160
beta90= -0.39651044278480513
beta = -0.3028813710872807


    
x90d0 = pulse.library.Drag(num_samples, amp90, sigma, beta90,name="Xp/2_d0")
    
xd0 = pulse.library.Drag(num_samples, amp, sigma, beta,name="Xp_d0")
yd0=pulse.library.Drag(num_samples, amp, sigma, beta,name="yp_d0")
y90d0=pulse.library.Drag(num_samples, amp90, sigma, beta90,name="yp_d0")

with pulse.build(backend,name='Custom_Not') as n_q0:
    
     pulse.play(x90d0, channel)
     #DD
     
     pulse.play(xd0,channel)#X
     pulse.delay(320,channel)
     pulse.shift_phase(pi, channel)
     pulse.shift_phase(pi, ControlChannel(1))
     pulse.play(xd0,channel)#Y
     pulse.delay(320,channel)
     pulse.play(xd0,channel)#X
     pulse.delay(320,channel)
     pulse.shift_phase(pi, channel)
     pulse.shift_phase(pi, ControlChannel(1))
     pulse.play(xd0,channel)#Y
     #XY4 End
     pulse.play(x90d0, channel)
     print('XY4')
     
     '''     #XY8 DD continued
     print('XY8')
     pulse.delay(320,channel)
     pulse.shift_phase(pi, channel)
     pulse.shift_phase(pi, ControlChannel(1))
     pulse.play(xd0,channel)#Y
     pulse.delay(320,channel)
     pulse.play(xd0,channel)#X
     pulse.delay(320,channel)
     pulse.shift_phase(pi, channel)
     pulse.shift_phase(pi, ControlChannel(1))
     pulse.play(xd0,channel)#Y
     pulse.delay(320,channel)
     pulse.play(xd0,channel)#X
     pulse.play(x90d0, channel)'''
     
     '''# Measurement in X bias
     print('x bias')
     pulse.play(x90d0,channel)'''
     
     # Measurement in y bias
     print('y bias')
     pulse.shift_phase(pi/2, channel) 
     pulse.shift_phase(pi/2, ControlChannel(1))
     pulse.play(y90d0, channel)#y/2
     pulse.shift_phase(-pi/2, channel)
     pulse.shift_phase(-pi/2, ControlChannel(1))

ngate=Gate(name='Custom_Not', label='X', num_qubits=1, params=[])

from qiskit import QuantumCircuit
qc = QuantumCircuit(1,1)
qc.append(ngate,[0])
qc.measure(0, 0)
    
qc.add_calibration('Custom_Not', [0], n_q0,[])
#qc.draw(output='mpl')
qct = transpile(qc, backend)
schedule(qct, backend).draw()
job=execute(qc, backend=backend, shots=8192, optimization_level=0)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
result=job.result()
counts = result.get_counts(qc)
print(counts)

from qiskit.tools.visualization import plot_histogram

#plot_histogram(result.get_counts(qc))
