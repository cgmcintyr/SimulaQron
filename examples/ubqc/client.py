import random
import struct
import sys
import time
from pathlib import Path

import numpy as np
from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

from flow import circuit_file_to_flow, count_qubits_in_sequence
from angle import measure_angle

# Randomly select circuit from circuits directory
circuits_path = Path(".") / "circuits"
circuit_file_paths = list(circuits_path.glob("*.json"))
circuit = random.choice(circuit_file_paths)

# Load circuit as MBQC flow
print("Client Loading {}".format(circuit))
seq_out = circuit_file_to_flow("./circuits/circuit1.json")

# Determine number of cubits our circuit needs
nQubits = count_qubits_in_sequence(seq_out)

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

# Outcome of each qubit will be stored in this outcome list
outcome = nQubits * [-1]

server_name = "Charlie"

with CQCConnection("Bob") as client:
    print("Client Sending (classical): Create {} qubits".format(nQubits))
    client.sendClassical(server_name, nQubits)

    angles = []
    for i in range(0, nQubits):
        rand_angle = int(256 * random.random())
        angles.append(rand_angle)
        q = qubit(client)
        q.rot_Y(64)  # |+> state
        q.rot_Z(rand_angle)
        print("Client Sending (quantum): qubit {}".format(i + 1))
        client.sendQubit(q, server_name)

    time.sleep(1)
    print("Client Sending (classical): Ask to perform {} measurements".format(nQubits))
    client.sendClassical(server_name, nMeasurement)
    time.sleep(1)
    print("Client Sending (classical): List of 1st Qubits to Entangle".format(nQubits))
    client.sendClassical(server_name, E1)
    time.sleep(1)
    print("Client Sending (classical): List of 2nd Qubits to Entangle".format(nQubits))
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

            print("Client Sending (classical): ask to measure qubit {}".format(qubit_n))
            time.sleep(1)
            client.sendClassical(server_name, qubit_n)

            print(
                "Client Sending (classical): measurement angle {}".format(angle_to_send)
            )
            time.sleep(1)
            client.sendClassical(server_name, angle_to_send)

            m = int.from_bytes(client.recvClassical(), "little")
            print("Client Received: result {}".format(m))

            # We adjust for the randomness only we know we added
            if r == 1:
                outcome[qubit_n - 1] = 1 - m
            else:
                outcome[qubit_n - 1] = m

    print("Client Output: {}".format(outcome))
    sys.exit(0)
