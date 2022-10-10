from qiskit import *
import matplotlib as plt
from numpy import *
qr=QuantumRegister(1)
cr=ClassicalRegister(1)
circuit=QuantumCircuit(qr,cr)
circuit.h(qr[0])
'''print('y bias')
circuit.ry(pi/2,0)# Y bias'''
#print('x bias')
#circuit.rx(pi/2,0)  #X bias
circuit.measure(qr,cr) 
#circuit.measure(qr[2],cr[2]) lot_histogram(result.get_counts(circuit))
#circuit.draw('mpl')
print('default')
#IBMQ.enable_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7')
IBMQ.save_account('5aa05e965118a4d4c39c15a864c922b90f9beacaa68818452d6d5bdc0a9642e3ebcec552361e81811e90133399c375cdceb726c0eebd8b318a5158259740b2f7',)
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
b='ibmq_quito'
print(b)
qcm=provider.get_backend(b)
#qcm=Aer.get_backend('qasm_simulator')
job=execute(circuit, backend=qcm, shots=8192, optimization_level=0)
from qiskit.tools.monitor import job_monitor
job_monitor(job)
result=job.result()
counts = result.get_counts(circuit)
print(counts)

from qiskit.tools.visualization import plot_histogram

#plot_histogram(result.get_counts(circuit))