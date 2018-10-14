from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *
import numpy as np
import random
import time
#from SimulaQron.virtnode.crudeSimulator.simpleEngine import *

from flow import circuit_file_to_flow, count_qubits_in_sequence
from angle import measure_angle
import struct

seq_out = circuit_file_to_flow("./circuits/circuit1.json")
nQubits= count_qubits_in_sequence(seq_out)
print("qubits needed: {}".format(nQubits))
print("----- out -----")

nMeasurement=0
E1=[]
E2=[]

for s in seq_out:
	s.printinfo()
	if s.type=="E":
		E1.append(s.qubits[0])
		E2.append(s.qubits[1])
	if s.type=="M":
		nMeasurement+=1
		#s.qubit
		
		
print(E1, E2)


print("Qubit number=", nQubits)

outcome=nQubits*[-1]
# Initialize the connection
with CQCConnection("client") as client:
	client.sendClassical('server', nQubits)
	angles=[]
	for i in range(0,nQubits):
		rand_angle=int(256*random.random())
		angles.append(rand_angle)
		q = qubit(client)
		q.rot_Y(64) #|+> state
		q.rot_Z(rand_angle)
		client.sendQubit(q,"server")

	time.sleep(1)
	client.sendClassical('server', nMeasurement)
	time.sleep(1)
	client.sendClassical('server', E1)
	time.sleep(1)
	client.sendClassical('server', E2)

		
	for s in seq_out:
		if s.type=="M":
			qubit_n= s.qubit
			print(qubit_n)
			computation_angle=s.angle
			input_angle=angles[qubit_n]	
			r=np.round(random.random())
			angle_to_send=measure_angle(qubit_n, seq_out, outcome, input_angle, computation_angle)+r*(np.pi)
			time.sleep(1)
			client.sendClassical('server', qubit_n)
			time.sleep(1)
			client.sendClassical('server', angle_to_send)
			m=int.from_bytes(client.recvClassical(),'little')	
			if r==1:
				outcome[qubit_n-1]=1-m
			else:
				outcome[qubit_n-1]=m		
			
			
	print(outcome)		
		#s.qubit

	
	
		#m=q.measure()
	
		
