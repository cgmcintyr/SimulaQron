from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

import sys

from collections import Iterable
from copy import deepcopy
from itertools import chain

import circuit


def _convert_gate_h(q1, q2, qubit_count):
    new_qubit = qubit_count + 1
    qubits = [[q1, q1, new_qubit], [new_qubit, 0, 0]]
    gates = ["E", "M", "X"]
    conditions = [0, 0, q1]
    return gates, qubits, conditions, new_qubit


def _convert_gate_cz(q1, q2, qubit_count):
    qubits = [[q1], [q2]]
    gates = ["E"]
    conditions = [0]
    return gates, qubits, conditions, qubit_count


def _convert_gate_x(q1, q2, qubit_count):
    qubits = [[q1], [0]]
    gates = ["X"]
    conditions = [0]
    return gates, qubits, conditions, qubit_count


def _convert_gate_z(q1, q2, qubit_count):
    qubits = [[q1], [0]]
    gates = ["Z"]
    conditions = [0]
    return gates, qubits, conditions, qubit_count


def _replace_qubit(qubits, old, new):
    qubits = deepcopy(qubits)
    for i, qubits_list in enumerate(qubits):
        for j, qubit in enumerate(qubits_list):
            if qubit == old:
                qubits[i][j] = new
    return qubits


def _convert(obj, gates, qubits, qubit_count):
    if len(gates) == 0:
        return obj

    gate = gates.pop(0)
    q1 = qubits[0].pop(0)
    q2 = qubits[1].pop(0)

    if gate == "H":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_h(
            q1, q2, qubit_count
        )
        if new_qubit_count != qubit_count:
            qubits = _replace_qubit(qubits, q1, new_qubit_count)
            qubit_count = new_qubit_count
    elif gate == "CZ":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_cz(
            q1, q2, qubit_count
        )
    elif gate == "X":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_x(
            q1, q2, qubit_count
        )
    elif gate == "Z":
        new_gates, new_qubits, new_conditions, new_qubit_count = _convert_gate_z(
            q1, q2, qubit_count
        )
    elif gate == "CX":
        # Defer conversion to next iterations
        gates += ["H", "CZ", "H"]
        qubits[0] += [q2, q1, q2]
        qubits[1] += [0, q2, 0]

        new_gates = []
        new_conditions = []
        new_qubits = [[], []]
    else:
        print("ERROR {}".format(gate))
        sys.exit(1)

    obj["gates"] += new_gates
    obj["qubits"][0] += new_qubits[0]
    obj["qubits"][1] += new_qubits[1]
    obj["conditions"] += new_conditions
    return _convert(obj, gates, qubits, qubit_count)


def convert(gates, qubits, qubit_count):
    empty = {"gates": [], "qubits": [[], []], "conditions": []}
    return _convert(empty, gates, qubits, qubit_count)


if __name__ == "__main__":
    qubit_count, gates, qubits = circuit.load("./circuits/circuit2.json")
    result = convert(gates, qubits, qubit_count)
    gates = result["gates"]
    qubits = result["qubits"]
    conditions = result["conditions"]
    print("gates: {}".format(gates))
    print("qubits: {}".format(qubits))
    print("conditions: {}".format(conditions))
