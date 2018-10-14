import numpy as np
def measure_angle(i, seq, outcome_array, input_angle, computation_angle):
    """Angle to measrue qubit i

    :i: qubit to measure
    :outcome_array: list of qubit outcomes
    :input_angle: random angle in radians that was generated for measuring
    :computation_angle: actual computation angle in radians (hidden by input_angle)
    """
    c = 0
    s = 0
    for gate in seq:
        if gate.type == "X" and gate.qubit == i:
            c += 0 if outcome_array[i] < 0 else outcome_array[i]
        elif gate.type == "Z" and gate.qubit == i:
            s += 0 if outcome_array[i] < 0 else outcome_array[i]
    return input_angle + (((-1) ** c) * (computation_angle)) + (s * 128)
