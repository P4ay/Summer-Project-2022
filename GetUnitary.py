# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 02:10:51 2022

@author: yashp
"""

from qiskit import *
import matplotlib as plt
from numpy import *
from qiskit.extensions import *
import math
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info.operators import Operator
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import Aer

backend = Aer.get_backend('unitary_simulator')

t=320
qreg_q = QuantumRegister(2, 'q')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)
q=[1,0]
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



#circuit.cx(q[0],q[1])
#circuit.rx(pi/2,q[0])

'''#circuit.barrier(q)
circuit.cu(pi/8,0,pi,0,q[0],q[1])#pi/8 
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])#X
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])
circuit.cu(pi/4,0,pi,0,q[0],q[1])#Pi/4
circuit.x(q[0])
circuit.delay(t,q[0])
circuit.barrier(q)
circuit.y(q[0])#Y
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.cu(pi/4,0,pi,0,q[0],q[1])#Pi/4
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])#X
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.x(q[0])
circuit.cu(pi/4,0,pi,0,q[0],q[1])#Pi/4
circuit.x(q[0])
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.y(q[0])#Y
circuit.barrier(q)
circuit.delay(t,q[0])
circuit.cu(pi/8,0,pi,0,q[0],q[1])#Pi/8
circuit.barrier(q)'''

job = backend.run(transpile(circuit, backend))
print(job.result().get_unitary(circuit, decimals=q[0]))
rho_AB = DensityMatrix.from_instruction(circuit)
print(rho_AB.draw())
