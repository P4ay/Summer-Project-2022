# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 17:44:32 2022

@author: yashp
"""

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
from qiskit import BasicAer

backend = BasicAer.get_backend('unitary_simulator')


qr=QuantumRegister(1)
cr=ClassicalRegister(1)
circuit=QuantumCircuit(qr,cr)


U1 = np.array([[0.92388, 0.382683 + 0j], [-0.382683, 0.92388 ]])
U2= np.array([[0.707107,- 0.707107j], [- 0.707107j, 0.707107 ]])
U3= np.array([[0.707107, - 0.707107j], [- 0.707107j, 0.707107]])
U4 = np.array([[0.92388 , -0.382683], [0.382683, 0.92388]])
circuit.unitary(U4, [0], label='U1')
circuit.unitary(U2, [0], label='U2')
circuit.unitary(U3, [0], label='U3')
circuit.unitary(U1, [0], label='U4')
#U5 = np.array([[1/math.sqrt(2), 1/math.sqrt(2)], [-(1/math.sqrt(2)), 1/math.sqrt(2)]])
#circuit.unitary(U5, [0], label='U5')
job = backend.run(transpile(circuit, backend))
print(job.result().get_unitary(circuit, decimals=3))
#qc.measure(qr[0], cr[0])
#plot_histogram(result.get_counts(circuit))