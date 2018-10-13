import json

def get_circuit(json_file):
	#read json 
	with open(json_file, "r") as circ:
		circuit=json.load(circ)
	nGates=len(circuit["gates"])
	gates=[];
	qubits=[]
	qubits_1=[];
	qubits_2=[];		
	for g in range(0,nGates):
		qubits=qubits+circuit["gates"][g]["qbits"]
		qubits_1=qubits_1+[circuit["gates"][g]["qbits"][0]]
		if len(circuit["gates"][g]["qbits"])==1:
			qubits_2=qubits_2+[0]
		else:
			qubits_2=qubits_2+[circuit["gates"][g]["qbits"][1]]
		gates=gates+[circuit["gates"][g]["type"]]
	
	nqbits=len(set(qubits))
	
	return nqbits,gates,qubits_1, qubits_2




