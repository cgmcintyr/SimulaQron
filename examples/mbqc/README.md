# MBQC

Interpret Flow notations MBQC as follows. There are four kinds of outputs:

* E [i,j]: entangle qubits i and j using Controlled Phase. 
* M i <img src="./docs/svgs/f50853d41be7d55874e952eb0d80c53e.svg" align=middle width=9.794565000000006pt height=22.831379999999992pt/> [m] [n]: Measurement angle for qubit i is <img src="./docs/svgs/5fc34debe9fe8c2254296f70d46bf923.svg" align=middle width=178.268805pt height=29.19113999999999pt/>
* X j i: Operation of conditional X on qubit j depending on measurement outcome of qubit i
* Z j i: Operation of conditional Z on qubit j depending on measurement outcome of qubit i
* X's and Z's can be accommodated in mesurement angle as such: <img src="./docs/svgs/17de0d63787245126004f04d9b080bea.svg" align=middle width=67.31604pt height=27.91271999999999pt/>: Measurement angle of qubit <img src="./docs/svgs/3369485e5fd1f281f6f6a547fa661280.svg" align=middle width=132.07309499999997pt height=24.65759999999998pt/>, where <img src="./docs/svgs/4fa3ac8fe93c68be3fe7ab53bdeb2efa.svg" align=middle width=12.356520000000005pt height=14.155350000000013pt/>, <img src="./docs/svgs/59efeb0f4f5d484a9b8a404d5bdac544.svg" align=middle width=14.971605000000004pt height=14.155350000000013pt/> are the measurement outcomes of qubits i and k respectively.

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


## Running Client and Server

We have a working UBMQC implementation with one client and one server. Please run the following:

```bash
git clone https://github.com/cgmcintyr/SimulaQron.git
cd SimulaQron
export PYTHONPATH=$(pwd):$PYTHONPATH
export NETSIM=$(pwd)
./run/startAll.sh
cd examples/mbqc/
python sever.py &
python client.py
```
