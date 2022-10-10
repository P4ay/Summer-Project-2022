# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 16:45:44 2022

@author: yashp
"""

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



from qiskit.pulse import library
    
q=3
t=320
with pulse.build(backend,name='DelayT') as d:
     pulse.delay(t,DriveChannel(q))
     pulse.delay(t,ControlChannel(q))
     
d_t=Gate(name='Delay_T', label='D_T', num_qubits=1, params=[])
from qiskit import QuantumCircuit
delay = QuantumCircuit(1,0)
delay.append(d_t,[0])
delay.add_calibration('d_t', [0], d,[])
dg_T=delay.to_gate( label='delay_T')

d_t2=Gate(name='Delay_t2', label='D_t2', num_qubits=1, params=[])
with pulse.build(backend,name='Delay_t2') as d_160:
     pulse.delay(t/2,DriveChannel(q))
     pulse.delay(t/2,ControlChannel(q))

from qiskit import QuantumCircuit
delay_t2 = QuantumCircuit(1,0)
delay_t2.append(d_t2,[0])
delay_t2.add_calibration('d_t2', [0], d_t2,[])
dg_T2=delay_t2.to_gate(label='delay_t2')

qc = QuantumCircuit(4,4)
qc.u(pi/4,pi,pi,q)#1
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.x(q)#X
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.u(pi/2,-pi/2,pi/2,q)#2
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.y(q)#Y
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.append(dg_T2,[q])
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.x(q)#X
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.u(pi/2,-pi/2,pi/2,q)#4
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.y(q)#Y
qc.barrier(q)
qc.append(dg_T,[q])
qc.barrier(q)
qc.u(pi/4,0,0,q)#5

#print('y bias')
#qc.ry(pi/2,q)
#print('x bias')
#qc.rx(pi/2,q)

qc.measure(q)
    
#qc.add_calibration('Custom_Not', [0], n_q0,[])
qc.draw(output='mpl')
IBMQ.save_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
b='ibmq_quito'
print(b)
backend=provider.get_backend(b)

qct = transpile(qc, backend)
schedule(qct, backend).draw()
job=execute(qc, backend=backend, shots=20000, optimization_level=0)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
result=job.result()
counts = result.get_counts(qc)
print(counts)

from qiskit.tools.visualization import plot_histogram

#plot_histogram(result.get_counts(qc))
