from SimulaQron.general.hostConfig import *
from SimulaQron.cqc.backend.cqcHeader import *
from SimulaQron.cqc.pythonLib.cqc import *

import time

from collections import Iterable
from copy import deepcopy
from itertools import chain

expected = {
    "gates": ["E", "M", "X"],
    "qubits": [[2, 2, 3, 1, 3, 3, 4], [3, 0, 0, 3, 4, 0, 0]],
    "conditions": [ 0, 0, 2 ]
}

original = {
    "gates": ["CZ", "H"],
    "qubits": [ [1, 2], [2, 0] ],
}

original = {
    "gates": ["H", "H"],
    "qubits": [[1, 1], [0, 0]],
}

def flatten(ls):
    def func(x):
        if isinstance(x, Iterable) and not isinstance(x, str): 
            return x
        return [x]
    return list(chain.from_iterable(func(x) for x in ls))

def convert(operations):
    operations = deepcopy(operations)
    operation_count = len(operations["gates"])
    hightest_qubit = max(list({ qubit for qubit in chain(*operations["qubits"])}))

    for op in range(operation_count):
        gate = operations["gates"][op]
        qubit1 = operations["qubits"][0][op]
        qubit2 = operations["qubits"][1][op]

        if gate == "H":
            operates_on = operations["qubits"][0][op]

            # Replace gates
            new_gates =  ["E", "M", "X"]
            operations["gates"][op] = new_gates

            # Replace qubits
            hightest_qubit += 1 # We need a new qubit
            new_qubits = [
                [operates_on, operates_on, hightest_qubit],
                [hightest_qubit, 0, 0,]
            ]
            operations["qubits"][0][op] = new_qubits[0]
            operations["qubits"][1][op] = new_qubits[1]

            # Replace all references to old qubit with new post-hadamard qubit
            for i, qubits_list in enumerate(operations["qubits"]):
                for j, qubit in enumerate(qubits_list[op:]):
                    if qubit == operates_on:
                        operations["qubits"][i][j] = hightest_qubit

            # New conditions/output
            new_conditions = [0,0,operates_on]
            conditions = operations.get("conditions", None)
            if not conditions:
                operations["conditions"] = new_conditions
            else:
                operations["conditions"].append(new_conditions)
        elif gate == "CZ":
            operations["gates"][op] = "E"
            conditions = operations.get("conditions", None)
            if not conditions:
                operations["conditions"] = [0]
            else:
                operations["conditions"].append(0)

    for i, row in enumerate(operations["qubits"]):
        operations["qubits"][i] = flatten(row)

    operations["gates"] = flatten(operations["gates"])
    operations["conditions"] = flatten(operations["conditions"])

    return operations

print(convert(original))
