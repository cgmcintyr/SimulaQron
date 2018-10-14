import sys
import json
from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *
#from SimulaQron.cqc.pythonLib.cqc import CQCConnection, CQCNoQubitError


qubits = []
num_measurements=4
outcome=[]

with CQCConnection("server") as Server:
	nQubits = Server.recvClassical()
	#Server.sendClassical("client",-1)
	nQubits=int.from_bytes(nQubits,byteorder='little')
	print("Server ", nQubits)

	for i in range(nQubits):
		qubits.append(Server.recvQubit())
	print (qubits)


	nMeasurement = Server.recvClassical()
	print(nMeasurement)
	#Server.sendClassical("client",-1)

	E1 = Server.recvClassical()
	print(E1)
	#Server.sendClassical("client",-1)
	
	E2 = Server.recvClassical()
	#Server.sendClassical("client",-1)
	print(E2)
	#entangle qubits
	for i, j in zip(E1, E2):
		qubits[i].CPHASE(qubits[j])

	
	
	for i in range(num_measurements):
		idx, angle = Server.recvClassical()
		qubits[idx].rot_Z(angle)
		m = qubits[idx].measure()
		Server.sendClassical('client', m)
	
	

