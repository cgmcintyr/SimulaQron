# Interpret Flow notations MBQC as follows. There are four kinds of outputs:

* E [i,j]: entangle qubits i and j using Controlled Phase. 
* M i $$\phi$$ [m] [n]: Measurement angle for qubit i is $$\alpha=(-1)^{\textnormal{(m mod 2)}}\phi+n\pi$$
* X j i: Operation of conditional X on qubit j depending on measurement outcome of qubit i
* Z j i: Operation of conditional Z on qubit j depending on measurement outcome of qubit i
* X's and Z's can be accommodated in mesurement angle as such: $$M_j^\alpha X_j^i Z_j^k$$: Measurement angle of qubit $$j=(-1)^{s_i} \alpha+s_k\pi$$, where $$s_i$$, $$s_k$$ are the measurement outcomes of qubits i and k respectively.
\end{itemize}

## Circuit JSON Documentation

We describe circuits to be encoded into MBQC format using a JSON file (see
examples in the `circuits` directory).

### Top Level Object

The file contains a single JSON object:

| Key   | Type                             | Descrption                    |
|-------|----------------------------------|-------------------------------|
| gates | list of gate objects (see below) | contains list of gate objects |

### Gate Objects

| Key    | Type                    | Descrption                                                                     |
|--------|-------------------------|--------------------------------------------------------------------------------|
| name   | string                  | name of gate to be created (does not have to be unique)                        |
| type   | string                  | "H", "CZ", "CX", "Z", or "X" (no other gates supported)                        |
| qubits | list of strings or ints | lists qubits the gate is applied to (2nd qubit is not necessary for H, X or Z) |
