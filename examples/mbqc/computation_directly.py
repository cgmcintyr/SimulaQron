from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *
from qutip import *

# from measurement import *

import json
import sys


def load_circuit(path):
    with open(path, "r") as circ:
        circuit = json.load(circ)
    nGates = len(circuit["gates"])
    gates = []
    qubits = []
    qubits_1 = []
    qubits_2 = []
    for g in range(0, nGates):
        qubits = qubits + circuit["gates"][g]["qbits"]
        qubits_1 = qubits_1 + [int(circuit["gates"][g]["qbits"][0])]
        if len(circuit["gates"][g]["qbits"]) == 1:
            qubits_2 = qubits_2 + [0]
        else:
            qubits_2 = qubits_2 + [int(circuit["gates"][g]["qbits"][1])]
        gates = gates + [circuit["gates"][g]["type"]]

    nqbits = len(set(qubits))
    return nGates, gates, qubits_1, qubits_2, nqbits


def do_clean_circuit(name, nGates, gates, qubits1, qubits2, nqbits):
    q = []
    for i in range(0, nqbits):
        q.append(qubit(name))

    for i in range(0, nGates):
        if gates[i] == "H":
            q[qubits1[i] - 1].H()
        if gates[i] == "CZ":
            q[qubits2[i] - 1].cphase(q[qubits1[i] - 1])
        if gates[i] == "X":
            q[qubits1[i] - 1].X()
        if gates[i] == "Z":
            q[qubits1[i] - 1].Z()
        if gates[i] == "CX":
            q[qubits2[i] - 1].cnot(q[qubits1[i] - 1])

    for i in range(0, nqbits):
        m = q[i].measure()
        print("qubit %d measure result:%d" % (i+1,m))



if __name__ == "__main__":
    result = load_circuit("./circuits/circuit4.json")
    nGates = result[0]
    gates = result[1]
    qubits1 = result[2]
    qubits2 = result[3]
    nqbits = result[4]
    print("nGates:", nGates)
    print("gates :  {}".format(", ".join(gates)))
    print("qubits1:", qubits1)
    print("qubits2:", qubits2)
    print("nqbits:", nqbits)

    # Initialise CQC connection
    Alice = CQCConnection("Alice")
    # q = qubit(Alice)
    # q.X()
    # result = Alice.tomography(qubit, 10)
    # q.H()
    # result = q.measure()
    # print("result:", result)
    do_clean_circuit(Alice, nGates, gates, qubits1, qubits2, nqbits)

    Alice.close()
