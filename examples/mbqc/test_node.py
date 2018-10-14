from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *
import numpy as np
import random
#from SimulaQron.virtnode.crudeSimulator.simpleEngine import *

from flow import circuit_file_to_flow, count_qubits_in_sequence

# Initialize the connection
with CQCConnection("client") as client:

	
	rand_angle=int(256*random.random())
	q = qubit(client)
	q.rot_Y(64) #|+> state
	q.rot_Z(rand_angle)
	m=q.measure()
	print(m)
		
