# Universal Blind Quantum Computation (UBQC)

The directory contains SimulaQron code for UBQC protocol for a partially quantum client (one who can prepare and send states) and single quantum server. It includes a classical subroutine to translate a quantum circuit into measuremnent language (meaurement.py) and hence convert it according to flow construction devised by  Elham Kashefi and Vincent Danos (flow.py). The output is then interpreted using UBQC protocol on the client side to assign (delegate) a full-fledged secret quantum computation to an all powerful quantum server. 

## MBQC

This subroutine takes input as decribed in the JSON file in the same repository described below. MBQC subroutine is composed of two functions, measurement.py and flow.py. The final output of the subroutine can be interpreted as follows:  

* E [i,j]: entangle qubits i and j using Controlled Phase. 
* M i <img src="./docs/svgs/f50853d41be7d55874e952eb0d80c53e.svg" align=middle width=9.794565000000006pt height=22.831379999999992pt/> [m] [n]: Measurement angle for qubit i is <img src="./docs/svgs/5fc34debe9fe8c2254296f70d46bf923.svg" align=middle width=178.268805pt height=29.19113999999999pt/>
* X j i: Operation of conditional X on qubit j depending on measurement outcome of qubit i
* Z j i: Operation of conditional Z on qubit j depending on measurement outcome of qubit i
* X's and Z's can be accommodated in mesurement angle as such: <img src="./docs/svgs/17de0d63787245126004f04d9b080bea.svg" align=middle width=67.31604pt height=27.91271999999999pt/>: Measurement angle of qubit <img src="./docs/svgs/3369485e5fd1f281f6f6a547fa661280.svg" align=middle width=132.07309499999997pt height=24.65759999999998pt/>, where <img src="./docs/svgs/4fa3ac8fe93c68be3fe7ab53bdeb2efa.svg" align=middle width=12.356520000000005pt height=14.155350000000013pt/>, <img src="./docs/svgs/59efeb0f4f5d484a9b8a404d5bdac544.svg" align=middle width=14.971605000000004pt height=14.155350000000013pt/> are the measurement outcomes of qubits i and k respectively.


## Running

```bash
git clone https://github.com/cgmcintyr/SimulaQron.git
cd SimulaQron
git checkout develop
export PYTHONPATH=$(pwd):$PYTHONPATH
export NETSIM=$(pwd)
./run/startAll.sh
cd examples/mbqc/
python sever.py &
python client.py
```


## Client/Server

### Client Design

The client will load a random circuit from the `circuits` directory. This circuit describes a computation the client wishes to perform.

Firstly the client converts the circuit into their measurement equivalents (see `measurements.py`), then converts these measurements into an MBQC flow that can be sent to the server (see `flow.py`).

The client then communicates with the server.

1. Client requests the server to reserve the number of random input qubits required for the measurements. Random qubits are introduced to hide the computation angle form the server
2. Client sends the entanglement information (from the output of MBQC subroutine) for the server to perform on the reserved qubits.
3. Client sends one measurement at a time, randomly adding an adjustment to the angle of measurement.  This is done to hide the output from the server. The client will make adjustments to their output to undo the random angle adjustments.
4. Client prints the output of its computation using the received classcial measurement outcome results.

### Server Design

The server was designed to accomodate the client, please see above.

The server can only handle one client at a time, and shuts itself down after a single UBQC has been completed.


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


## Authors

This example was created at the RIPE NCC Quantum Internet Hackathon 2018 by Team aMBiQuiCy.

The team members were:

* Andrey Hoursanov
* Anne Marin
* Christopher McIntyre
* Georg Harder
* Marc Ibrahim
* Shraddha Singh
* Yao Ma
