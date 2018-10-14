import sys
import json
from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *
#from SimulaQron.cqc.pythonLib.cqc import CQCConnection, CQCNoQubitError
import time
import struct

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
                print("i: {}, j: {}".format(i,j))
                qubit_i = qubits[i - 1]
                qubit_j = qubits[j - 1]
                qubit_i.cphase(qubit_j)

	
	nMeasurement=int.from_bytes(nMeasurement,byteorder='little')
	for i in range(nMeasurement):
		qubit_n=int.from_bytes(Server.recvClassical(),'little')
		angle=int.from_bytes(Server.recvClassical(),'little')
		print ("qubit to measure", qubit_n)
		print ("angle of measurement", angle)
		qubits[qubit_n].rot_Z(angle)
		m = qubits[qubit_n].measure()
		time.sleep(1)
		Server.sendClassical('client', m)
	
	

