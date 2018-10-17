from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *
import numpy as np
import random
import time

# from SimulaQron.virtnode.crudeSimulator.simpleEngine import *

from flow import circuit_file_to_flow, count_qubits_in_sequence
from angle import measure_angle
import struct

# Load circuit from JSON file
seq_out = circuit_file_to_flow("./circuits/circuit1.json")

# Determine number of cubits our circuit needs
nQubits = count_qubits_in_sequence(seq_out)
print("qubits needed: {}".format(nQubits))
print("----- out -----")

# Initialize measurements count and entanglement lists
nMeasurement = 0
E1 = []
E2 = []

# We use the flow sequence to build entanglemtn lists and count measurements
for s in seq_out:
    s.printinfo()
    if s.type == "E":
        E1.append(s.qubits[0])
        E2.append(s.qubits[1])
    if s.type == "M":
        nMeasurement += 1
        # s.qubit

# Outcome of each qubit will be stored in this outcome list
outcome = nQubits * [-1]

server_name = "Charlie"


with CQCConnection("Bob") as client:
    print("Sending: Create {} qubits".format(nQubits))
    client.sendClassical(server_name, nQubits)

    angles = []
    for i in range(0, nQubits):
        rand_angle = int(256 * random.random())
        angles.append(rand_angle)
        q = qubit(client)
        q.rot_Y(64)  # |+> state
        q.rot_Z(rand_angle)
        print("Sending qubit: {} to {}".format(i+1, server_name))
        client.sendQubit(q, server_name)

    time.sleep(1)
    print("Sending: Ask to perform {} measurements".format(nQubits))
    client.sendClassical(server_name, nMeasurement)
    time.sleep(1)
    print("Sending: List of 1st Qubits to Entangle".format(nQubits))
    client.sendClassical(server_name, E1)
    time.sleep(1)
    print("Sending: List of 2nd Qubits to Entangle".format(nQubits))
    client.sendClassical(server_name, E2)

    for s in seq_out:
        if s.type == "M":
            # Which qubit are we measuring?
            qubit_n = s.qubit

            # What is the angle we wish to measure
            computation_angle = s.angle
            input_angle = angles[qubit_n]

            # Calclate the angle to send with randomisation applied
            r = np.round(random.random())
            angle_to_send = measure_angle(
                qubit_n, seq_out, outcome, input_angle, computation_angle
            ) + r * (np.pi)

            print("Sending: ask to measure qubit {}".format(qubit_n))
            time.sleep(1)
            client.sendClassical(server_name, qubit_n)

            print("Sending: measurement angle {}".format(angle_to_send))
            time.sleep(1)
            client.sendClassical(server_name, angle_to_send)

            m = int.from_bytes(client.recvClassical(), "little")
            print("Received: result {}".format(m))

            # We adjust for the randomness only we know we added
            if r == 1:
                outcome[qubit_n - 1] = 1 - m
            else:
                outcome[qubit_n - 1] = m

    print("Output of circuit: {}".format(outcome))
