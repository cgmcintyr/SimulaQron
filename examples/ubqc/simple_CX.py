from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *
import numpy as np
import random
from angle import measure_angle
#from SimulaQron.virtnode.crudeSimulator.simpleEngine import *

from flow import circuit_file_to_flow, count_qubits_in_sequence



    

seq_out = circuit_file_to_flow("./circuits/circuit_CX.json")
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
		
		
#print(E1, E2)


print("Qubit number=", nQubits)

real_qubits = []

measurement_outcomes = -1*np.ones(nQubits)




# Initialize the connection
with CQCConnection("client") as client:
	
	
	q = qubit(client)
	real_qubits.append(q)

	q = qubit(client)
	real_qubits.append(q)
	

	for i in range(2,nQubits):
		q = qubit(client)
		q.rot_Y(64) #|+> state
		real_qubits.append(q)

	for i,j in zip(E1,E2):
		real_qubits[i-1].cphase(real_qubits[j-1])



	for s in seq_out:
		if s.type=='E':
			continue
		elif s.type=='M':
			input_angle = s.angle
			angle = measure_angle(s.qubit-1, seq_out, measurement_outcomes, input_angle, 0)
			q.rot_Z(int(angle/2/np.pi*256))
			q.rot_Y(256-64)
			measurement_outcomes[s.qubit-1] = real_qubits[s.qubit-1].measure()
		elif s.type=='Z':
			power = measurement_outcomes[s.power_idx-1]
			if power == 1:
				q.Z
		elif s.type=='X':
			power = measurement_outcomes[s.power_idx-1]
			if power == 1:
				q.X
		print(s.type)
		print(measurement_outcomes)


	# measure 6 and 8
	#real_qubits[0].H()
	real_qubits[0].rot_Y(256-64)
	measurement_outcomes[0] = real_qubits[0].measure()
	real_qubits[3].rot_Y(256-64)
	measurement_outcomes[3] = real_qubits[3].measure()
	

print(measurement_outcomes)


