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

client_name = "Bob"

with CQCConnection("Charlie") as Server:
    # Client first defines number of qubits needed for their circuit
    nQubits = Server.recvClassical()
    nQubits = int.from_bytes(nQubits, byteorder="little")
    print("Server Received (classical): Create {} qubits".format(nQubits))

    # We need to receive all qubits from client
    for i in range(nQubits):
        qubits.append(Server.recvQubit())
    print("Server Received (quntum): qubits received")

    # Client next defines the number of measurments to be performed
    nMeasurement = Server.recvClassical()
    nMeasurement = int.from_bytes(nMeasurement, byteorder="little")
    print(
        "Server Received (classical): Client asking to perform {} measurements".format(
            nQubits
        )
    )

    # First step of MBQC is entangling qubits into a graph state
    E1 = Server.recvClassical()
    print("Server Received (classical): List of 1st Qubits to Entangle".format(nQubits))
    E2 = Server.recvClassical()
    print("Server Received (classical): List of 2nd Qubits to Entangle".format(nQubits))
    print("Server Entangling...")
    for i, j in zip(E1, E2):
        qubit_i = qubits[i - 1]
        qubit_j = qubits[j - 1]
        qubit_i.cphase(qubit_j)

    # Server is ready to measure!
    print("Server Measuring...")
    for i in range(nMeasurement):
        # Each measurement has has a qubit index (between 0 and nQubits)
        qubit_n = int.from_bytes(Server.recvClassical(), "little")
        # Each measurement has an angle to measure in degrees
        angle = int.from_bytes(Server.recvClassical(), "little")

        print("Server Measuring qubit {} using angle {}".format(qubit_n, angle))
        qubits[qubit_n].rot_Z(angle)
        m = qubits[qubit_n].measure()

        time.sleep(1)
        print("Server Sending (classical): result of measurement to client")
        Server.sendClassical(client_name, m)

    sys.exit(0)
