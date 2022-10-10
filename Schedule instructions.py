from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
# Import qiskit packages
from qiskit import IBMQ
from qiskit import schedule, transpile
from qiskit.tools.monitor import job_monitor
import numpy as np 
from numpy import *

qc = QuantumCircuit(2,2) #difining circuit 
#qc.y(0)
#qc.barrier(0)
#qc.rx(pi/2,0)
#qc.u2(pi,pi/3,0)
qc.h(0)
qc.barrier()
qc.cx(0,1)
'''qc.barrier(0)
qc.x(0)
qc.barrier(0)
qc.y(0)
qc.barrier(0)
qc.rx(pi/2,0)'''
#qc.rx(pi,0)
#qc.rx(pi,0)
#qc.y(0)
#qc.draw('mpl')
#qc.measure(0,0)
#qc.measure(1,1)


from qiskit import pulse
IBMQ.save_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7')
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend=provider.get_backend('ibmq_belem')
qct = transpile(qc, backend)
schedule(qct, backend).draw()
print(schedule(qct, backend).instructions)