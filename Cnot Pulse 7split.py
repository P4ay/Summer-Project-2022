from qiskit import pulse
from qiskit.pulse import Acquire, AcquireChannel, MemorySlot, ControlChannel, DriveChannel
from qiskit import IBMQ
from qiskit import schedule, transpile, execute
from qiskit.tools.monitor import job_monitor
from qiskit.circuit import Gate
import numpy as np
import warnings
from qiskit.visualization import plot_state_city, plot_bloch_multivector, plot_histogram
from qiskit.tools.visualization import plot_histogram,plot_state_city, plot_bloch_vector,plot_state_qsphere
warnings.filterwarnings('ignore')


dc0 = DriveChannel(0)
dc1 = DriveChannel(1)
cc0 = ControlChannel(0)
cc1 = ControlChannel(1)

IBMQ.save_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend=provider.get_backend('ibmq_belem')

from qiskit.pulse import library


#Pulse parameter values
x90amp = 0.12254867310389062+0.005568708580629559j
x90sigma = 40
x90num_samples = 160
x90beta= -2.472825975940949

h = pulse.library.Drag(x90num_samples, x90amp, x90sigma, x90beta,name="x90_q0")


y90amp=-0.005568708580629555+0.12254867310389062j
y90sigma=40
y90beta=-2.4909884222108594
y90num_samples=160
y90 = pulse.library.Drag(y90num_samples, y90amp, y90sigma, y90beta,name="y90")

x90q1amp = 0.11945361026742672+0.0022819639833625035j
x90q1sigma = 40
x90q1num_samples = 160
x90q1beta= 0.6983177108024056
x90q1 = pulse.library.Drag(x90q1num_samples, x90q1amp, x90q1sigma, x90q1beta,name="x90_q1")

cr90d0duration=1584
cr90d0amp=0.02217448201775707+0.0041181718791566445j
cr90d0sigma= 64
cr90d0width= 1328
cr90p_d0_u1=pulse.library.GaussianSquare(cr90d0duration, cr90d0amp, cr90d0sigma, cr90d0width,name="CR90_d0_u1")

cr45p_d0_u1=pulse.library.GaussianSquare(cr90d0duration, cr90d0amp/2, cr90d0sigma, cr90d0width,name="CR45_d0_u1")

cr90duration=1584
cr90amp=-0.13646570704963157+0.04816083129856447j
cr90sigma= 64
cr90width= 1328
cr90p_u1=pulse.library.GaussianSquare(cr90duration, cr90amp, cr90sigma, cr90width,name="CR90p_u1")

cr45p_u1=pulse.library.GaussianSquare(cr90duration, cr90amp/2, cr90sigma, cr90width,name="CR45p_u1")

xpq1amp =0.24595349979957964+0j
xpq1sigma = 40
xpq1num_samples = 160
xpq1beta= 0.6612108242016485
xpq1 = pulse.library.Drag(xpq1num_samples, xpq1amp, xpq1sigma, xpq1beta,name="xp_q1")

cr90md0amp=-0.02217448201775707-0.004118171879156642j
cr90m_d0_u1=pulse.library.GaussianSquare(cr90d0duration, cr90md0amp, cr90d0sigma, cr90d0width,name="CR90m_d0_u1")

cr45m_d0_u1=pulse.library.GaussianSquare(cr90d0duration, cr90md0amp/2, cr90d0sigma, cr90d0width,name="CR45m_d0_u1")


cr90mamp=0.13646570704963157-0.04816083129856449j
cr90m_u1=pulse.library.GaussianSquare(cr90duration, cr90mamp, cr90sigma, cr90width,name="CR90m_u1")

cr45m_u1=pulse.library.GaussianSquare(cr90duration, cr90mamp/2, cr90sigma, cr90width,name="CR45_d0_u1")

y90mamp=0.002281963983362441-0.11945361026742674j
y90mbeta=0.6983177108024056
y90m = pulse.library.Drag(y90num_samples, y90mamp, y90sigma, y90mbeta,name="y90")


    
with pulse.build(backend,name='Cnot start') as cns:

    pulse.shift_phase(-3.141592653589793, dc0)
    pulse.shift_phase(-1.5707963267948966, dc0)
    pulse.shift_phase(-1.5707963267948966, dc1)
    pulse.shift_phase(-1.5707963267948966, cc0)  
    pulse.shift_phase(-1.5707963267948966, cc1)
    pulse.shift_phase(-1.5707963267948966, ControlChannel(4))
    pulse.shift_phase(-1.5707963267948966, ControlChannel(5)) 
    #pulse.delay(160,dc1)
    pulse.play(y90,dc0)
    pulse.play(x90q1,dc1)
    pulse.delay(160,cc1)
    pulse.shift_phase(-3.141592653589793, cc1)
    
with pulse.build(backend,name='cr22') as cr22p1:
    pulse.play(cr45p_d0_u1,dc0)
    pulse.play(cr45p_u1, cc1)
    pulse.delay(1584,dc1)

with pulse.build(backend,name='cr22p') as cr22p2:    
    pulse.play(cr45p_d0_u1,dc0)
    pulse.play(cr45p_u1, cc1)
    pulse.delay(1584,dc1)
    
with pulse.build(backend,name='mid X') as X:        
    pulse.play(xpq1,dc1)
    pulse.delay(160,dc0)
    pulse.delay(160,cc1)
    
with pulse.build(backend,name='cr22m') as cr22m1:            
    pulse.play(cr45m_d0_u1,dc0)
    pulse.play(cr45m_u1,cc1)    
    pulse.delay(1584,dc1)
    
with pulse.build(backend,name='cr22m') as cr22m2:            
    pulse.play(cr45m_d0_u1,dc0)
    pulse.play(cr45m_u1,cc1)
    pulse.delay(1584,dc1)

with pulse.build(backend,name='Cnot end') as cne:                
    pulse.shift_phase(-1.5707963267948966, dc0)  
    pulse.shift_phase(-1.5707963267948966, cc1)
    pulse.play(h,dc0)
    pulse.play(y90m,dc1)
#    pulse.acquire(m, pulse.acquire_channel(0), MemorySlot(0))'''

#Creating Pulse Gates
cn_s=Gate(name='cnot_start', label='cns', num_qubits=2, params=[])
cr22_p1=Gate(name='cr22p1', label='cr22', num_qubits=2, params=[])
#cr22_p2=Gate(name='cr22p2', label='cr22', num_qubits=2, params=[])
m_X=Gate(name='X_mid', label='X', num_qubits=2, params=[])
cr22_m1=Gate(name='cr22m1', label='-cr22', num_qubits=2, params=[])
#cr22_m2=Gate(name='cr22m2', label='-cr22', num_qubits=2, params=[])
cn_e=Gate(name='Cnot_end', label='cne', num_qubits=2, params=[])

#Creating circuit
from qiskit import QuantumCircuit
qc = QuantumCircuit(2,2)
qc.h(0)
qc.append(cn_s, [0,1])
qc.append(cr22_p1, [0,1])
qc.append(cr22_p1, [0,1])
qc.append(m_X, [0,1])
qc.append(cr22_m1, [0,1])
qc.append(cr22_m1, [0,1])
qc.append(cn_e, [0,1])
qc.measure(0,0) 
qc.measure(1,1)

#adding calibration
qc.add_calibration('cnot_start', [0,1], cns,[])
qc.add_calibration('cr22p1', [0,1], cr22p1,[])
#qc.add_calibration('cr22p2', [0,1], cr22p2,[])
qc.add_calibration('X_mid', [0,1], X,[])
qc.add_calibration('cr22m1', [0,1], cr22m1,[])
#qc.add_calibration('cr22m2', [0,1], cr22m2,[])
qc.add_calibration('Cnot_end', [0,1], cne,[])
#qc.add_calibration('cn_gate', [0,1], cn_gate_pulse )


qct = transpile(qc, backend)
#qct.draw(output='mpl')
schedule(qct, backend).draw()

job=execute(qc, backend=backend, shots=20000, optimization_level=0)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
result=job.result()
counts = result.get_counts(qc)
print(counts)


#plot_histogram(result.get_counts(qc))
#psi  = result.get_statevector(qc)
#print(psi)
#plot_state_qsphere(psi)
#plot_state_city(psi)
#plot_bloch_multivector(psi)'''