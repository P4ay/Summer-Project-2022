# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 00:31:17 2022

@author: yashp
"""

from qiskit import QuantumCircuit
from qiskit import Aer, transpile
from qiskit.tools.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi
Aer.backends()
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
from qiskit import *


simulator = Aer.get_backend('aer_simulator')

t=320
print('CNOT XY4')
qreg_q = QuantumRegister(5, 'q')
creg_c = ClassicalRegister(5, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
q=[3,4]

circuit.h(q[0])
circuit.barrier(q)
circuit.cu(pi/8,0,pi,0,q[0],q[1])#pi/8
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])#X
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])
circuit.cu(pi/4,0,0,0,q[0],q[1])#Pi/4
circuit.x(q[0])
circuit.delay(t,q[0])
circuit.barrier(q)
circuit.y(q[0])#Y
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.cu(pi/4,0,0,0,q[0],q[1])#Pi/4
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])#X
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])
circuit.cu(pi/4,0,0,0,q[0],q[1])#Pi/4
circuit.x(q[0])
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.y(q[0])#Y
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.cu(pi/8,0,0,0,q[0],q[1])#pi/8
circuit.barrier(q)
#print('u2')
#circuit.h(q[0])

#print('u3')
#circuit.rx(pi/2,q[0])

#print('u4')
#circuit.h(q[1])

#print('u5')
#circuit.rx(pi/2,q[1])

#print('u6')
#circuit.cx(q[0],q[1])
#circuit.h(q[0])

print('u7')
circuit.cx(q[0],q[1])
circuit.rx(pi/2,q[0])

#circuit.crx(pi / 8, qreg_q[3], qreg_q[4])
#circuit.measure(qr[0], cr[0])
#plot_histogram(result.get_counts(circuit))
#circuit.draw('mpl')



circuit.measure(q,q)


 
#IBMQ.save_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7')
#IBMQ.load_account()
#provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
#b='ibmq_quito'
#print(b)
backend= Aer.get_backend('aer_simulator')


qct = transpile(circuit, backend)
#schedule(qct, backend).draw()
job=execute(circuit, backend=backend, shots=20000, optimization_level=0)
#print(job.name)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
result=job.result()
counts = result.get_counts(circuit)
print(counts)