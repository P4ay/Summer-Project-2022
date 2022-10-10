# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 16:49:56 2022

@author: yashp
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 16:45:44 2022

@author: yashp
"""
from qiskit import QuantumCircuit
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
import numpy as np

channel = DriveChannel(0)



from qiskit.pulse import library
    
q=3
t=320

sx = np.array([[0, 1], [1, 0]]);
sy = np.array([[0, -1j], [1j, 0]]);
sz = np.array([[1, 0], [0, -1]]);
def euler(a):
    return(np.cos(a)+np.sin(a)*1j)


U1= np.array([[1 , 0 ], [0 ,1 ]])
U2= np.array([[1/2*(euler(-pi/8))+1/2*(euler(pi/8 )) ,0.5j*(euler(-pi/8 )) -0.5j*(euler(pi/8 )) ], [-0.5j*(euler(-pi/8 )) +0.5j*(euler(pi/8 )), 1/2*(euler(-pi/8 ))+1/2*(euler(pi/8 )) ]])
U3= np.array([[1/2*(euler(-pi/8))+1/2*(euler(pi/8 )) ,-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  ], [-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  , 1/2*(euler(-pi/8 ))+1/2*(euler(pi/8 )) ]])
U4= np.array([[1/2*(euler(-pi/8))+1/2*(euler(pi/8 )) ,-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  ], [-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  , 1/2*(euler(-pi/8 ))+1/2*(euler(pi/8 )) ]])
U5= np.array([[1 , 0 ], [0 ,1 ]])
U6= np.array([[1/2*(euler(-pi/8))+1/2*(euler(pi/8 )) ,-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  ], [-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  , 1/2*(euler(-pi/8 ))+1/2*(euler(pi/8 )) ]])
U7= np.array([[1/2*(euler(-pi/8))+1/2*(euler(pi/8 )) ,-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  ], [-0.5*(euler(-pi/8 )) +0.5*(euler(pi/8 ))  , 1/2*(euler(-pi/8 ))+1/2*(euler(pi/8 )) ]])
U8= np.array([[1/2*(euler(-pi/8))+1/2*(euler(pi/8 )) ,-0.5j*(euler(-pi/8 )) +0.5j*(euler(pi/8 )) ], [0.5j*(euler(-pi/8 )) -0.5j*(euler(pi/8 )), 1/2*(euler(-pi/8 ))+1/2*(euler(pi/8 )) ]])
U9= np.array([[1 , 0 ], [0 ,1 ]])

qc=QuantumCircuit(q+1,q+1)
qc.barrier(q)
qc.unitary(U9, [q], label='U9')
qc.delay(t/2,q)
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sx, [q], label='X')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U8, [q], label='U8')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sy, [q], label='Y')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U7, [q], label='U7')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sx, [q], label='X')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U6, [q], label='U6')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sy, [q], label='Y')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U5, [q], label='U5')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sy, [q], label='Y')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U4, [q], label='U4')#'''
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sx, [q], label='X')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U3, [q], label='U3')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sy, [q], label='Y')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U2, [q], label='U2')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(sx, [q], label='X')
qc.barrier(q)
qc.delay(t,q)
qc.barrier(q)
qc.unitary(U1, [q], label='U1')
qc.delay(t/2,q)
qc.barrier(q)
#print('y bias')
#qc.ry(pi/2,q)
#print('x bias')
#qc.rx(pi/2,q)

qc.measure(q,q)
    
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
print(job.name)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
result=job.result()
counts = result.get_counts(qc)
print(counts)

#from qiskit.tools.visualization import plot_histogram

#plot_histogram(result.get_counts(qc))
