import sys
import json
from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

# from SimulaQron.cqc.pythonLib.cqc import CQCConnection, CQCNoQubitError
import time
import struct

qubits = []
num_measurements = 4
outcome = []



with CQCConnection("server") as Server:
    # Client first defines number of qubits needed for their circuit
    nQubits = Server.recvClassical()
    nQubits = int.from_bytes(nQubits, byteorder="little")
    print("Received: Create {} qubits".format(nQubits))

    for i in range(nQubits):
        qubits.append(Server.recvQubit())
    print("Created Qubits")

    nMeasurement = Server.recvClassical()
    nMeasurement = int.from_bytes(nMeasurement, byteorder="little")
    print("Received: Client asking to perform {} measurements".format(nQubits))

    E1 = Server.recvClassical()
    print("Received: List of 1st Qubits to Entangle".format(nQubits))

    E2 = Server.recvClassical()
    print("Received: List of 2nd Qubits to Entangle".format(nQubits))

    # entangle qubits
    print("Entangling...")
    for i, j in zip(E1, E2):
        qubit_i = qubits[i - 1]
        qubit_j = qubits[j - 1]
        qubit_i.cphase(qubit_j)

    print("Measuring...")
    for i in range(nMeasurement):
        qubit_n = int.from_bytes(Server.recvClassical(), "little")
        angle = int.from_bytes(Server.recvClassical(), "little")
        print("Measuring qubit {} using angle {}".format(qubit_n, angle))
        qubits[qubit_n].rot_Z(angle)
        m = qubits[qubit_n].measure()
        time.sleep(1)
        print("Sending result of measurement to client")
        Server.sendClassical("client", m)
