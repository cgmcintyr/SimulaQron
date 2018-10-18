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
            c += outcome_array[i] 
            elif gate.type == "Z" and gate.qubit == i:
            s += outcome_array[i]  
        elif gate.type=="M" and gate.qubit==i:
                c+=gate.X_idxs    #takes into account the extra arrays of M which contained xtra Xs due to commutation
        elif gate.type=="M" and gate.qubit==i:
                s+=gate.Z_idxs  #same for Z

                return input_angle + (((-1) ** c) * (computation_angle) + (s * 128) #SimulaQron takes one step of angle as pi/255, hence the given description
