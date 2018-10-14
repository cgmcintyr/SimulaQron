import numpy as np
from measurement import convert
import circuit
from copy import deepcopy


class Gate:
    """Represents gate being applied to qubits/conditions"""

    def __init__(self, gate_type, args):
        self.type = gate_type
        if gate_type == "E":
            self.qubits = args[0]
        elif gate_type == "M":
            self.qubit = args[0]
            self.angle = args[1]
            self.X_idxs = []
            self.Z_idxs = []
        elif gate_type == "X":
            self.qubit = args[0]
            self.power_idx = args[1]
        elif gate_type == "Z":
            self.qubit = args[0]
            self.power_idx = args[1]
        elif gate_type == "R":
            self.qubit = args[0]
            self.angle = args[1]
            self.axis = args[2]

    def printinfo(self):
        if self.type == "E":
            print(self.type, self.qubits)
        elif self.type == "M":
            print(self.type, self.qubit, self.angle, self.X_idxs, self.Z_idxs)
        elif self.type == "X":
            print(self.type, self.qubit, self.power_idx)
        elif self.type == "Z":
            print(self.type, self.qubit, self.power_idx)


def construct_flow_from_sequence(seq):
    seq = deepcopy(seq)
    N = len(seq)
    i = 1
    while i < N:
        # print(i)
        if seq[i].type == "E":
            if seq[i - 1].type == "E":
                i = i + 1
                continue

            if (seq[i - 1].type == "Z") | (
                (seq[i].qubits[0] != seq[i - 1].qubit)
                & (seq[i].qubits[1] != seq[i - 1].qubit)
            ):
                # print('condition E commute')
                seq[i - 1], seq[i] = seq[i], seq[i - 1]
                i = i - 1
                continue
            elif seq[i - 1].type == "X":
                if seq[i].qubits[0] == seq[i - 1].qubit:
                    # print('condition 1')
                    seq[i - 1], seq[i] = seq[i], seq[i - 1]
                    seq.insert(i, Gate("Z", [seq[i - 1].qubits[1], seq[i].power_idx]))
                    i = i - 1
                    N = len(seq)
                    continue
                elif seq[i].qubits[1] == seq[i - 1].qubit:
                    # print('condition 2')
                    seq[i - 1], seq[i] = seq[i], seq[i - 1]
                    seq.insert(i, Gate("Z", [seq[i - 1].qubits[0], seq[i].power_idx]))
                    i = i - 1
                    N = len(seq)
                    continue

        elif seq[i].type == "M":
            if (seq[i - 1].type == "M") | (seq[i - 1].type == "E"):
                i = i + 1
                continue
            elif seq[i].qubit != seq[i - 1].qubit:
                # print('condition M commute')
                seq[i - 1], seq[i] = seq[i], seq[i - 1]
                i = i - 1
                continue
            elif seq[i - 1].type == "X":
                # print('condition X++')
                seq[i].X_idxs.append(i - 1)
                del seq[i - 1]
                N = len(seq)
                i = i - 1
                continue
            elif seq[i - 1].type == "Z":
                # print('condition Z++')
                seq[i].Z_idxs.append(i - 1)
                del seq[i - 1]
                N = len(seq)
                i = i - 1
                continue

        i = i + 1
        N = len(seq)

    return seq


def _measurement_dictionary_to_sequence(dictionary):
    seq = []
    gates = dictionary["gates"]
    qubits = dictionary["qubits"]
    conditions = dictionary["conditions"]

    for i in range(len(gates)):
        if gates[i] == "E":
            seq.append(Gate("E", [[qubits[0][i], qubits[1][i]]]))
        elif gates[i] == "M":
            seq.append(Gate("M", [qubits[0][i], conditions[i]]))
        elif gates[i] in ("X", "Y", "Z"):
            seq.append(Gate(gates[i], [qubits[0][i], conditions[i]]))

    return seq


if __name__ == "__main__":
    qubit_count, gates, qubits = circuit.load("./circuits/circuit1.json")
    result = convert(gates, qubits, qubit_count)
    seq_in = _measurement_dictionary_to_sequence(result)
    seq_out = construct_flow_from_sequence(seq_in)

    print("---- in ------")
    for s in seq_in:
        s.printinfo()
    print("----- out -----")
    for s in seq_out:
        s.printinfo()
