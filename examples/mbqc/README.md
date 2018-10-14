# Interpret Flow notations MBQC as follows. There are four kinds of outputs:

* E [i,j]: entangle qubits i and j using Controlled Phase. 
* M i <img src="https://raw.githubusercontent.com/cgmcintyr/SimulaQron/develop/examples/mbqc/docs/svgs/f50853d41be7d55874e952eb0d80c53e.svg?invert_in_darkmode" align=middle width=9.794565000000006pt height=22.831379999999992pt/> [m] [n]: Measurement angle for qubit i is <p align="center"><img src="https://raw.githubusercontent.com/cgmcintyr/SimulaQron/develop/examples/mbqc/docs/svgs/735e8de2fd41b658155c484dad1d35d9.svg?invert_in_darkmode" align=middle width=178.2693pt height=19.526925pt/></p>
* X j i: Operation of conditional X on qubit j depending on measurement outcome of qubit i
* Z j i: Operation of conditional Z on qubit j depending on measurement outcome of qubit i
* X's and Z's can be accommodated in mesurement angle as such: <p align="center"><img src="https://raw.githubusercontent.com/cgmcintyr/SimulaQron/develop/examples/mbqc/docs/svgs/005752769365b80b615b7759adcc1e7f.svg?invert_in_darkmode" align=middle width=67.31604pt height=21.07941pt/></p>: Measurement angle of qubit <p align="center"><img src="https://raw.githubusercontent.com/cgmcintyr/SimulaQron/develop/examples/mbqc/docs/svgs/2d626711053a6cd4497bb9137817e32a.svg?invert_in_darkmode" align=middle width=132.073095pt height=16.438356pt/></p>, where <p align="center"><img src="https://raw.githubusercontent.com/cgmcintyr/SimulaQron/develop/examples/mbqc/docs/svgs/330c76e2bed5ef9884b787c69a74bfb4.svg?invert_in_darkmode" align=middle width=12.3563715pt height=9.5433525pt/></p>, <p align="center"><img src="https://raw.githubusercontent.com/cgmcintyr/SimulaQron/develop/examples/mbqc/docs/svgs/dcd583c614e714f274ddf2d2b531621b.svg?invert_in_darkmode" align=middle width=14.971505999999998pt height=9.5433525pt/></p> are the measurement outcomes of qubits i and k respectively.
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
