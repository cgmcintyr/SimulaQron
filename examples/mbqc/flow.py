import numpy as np
from measurement import convert
import circuit





class Gate():
	"""docstring for gate"""
	def __init__(self, gate_type, args):
		self.type = gate_type
		if gate_type == 'E':
			self.qubits = args[0]
		elif gate_type == 'M':
			self.qubit = args[0]
			self.angle = args[1]
			self.X_idxs = []
			self.Z_idxs = []
		elif gate_type == 'X':
			self.qubit = args[0]
			self.power_idx = args[1]
		elif gate_type == 'Z':
			self.qubit = args[0]
			self.power_idx = args[1]
		elif gate_type == 'R':
			self.qubit = args[0]
			self.angle = args[1]
			self.axis = args[2]
	def printinfo(self):
		if self.type == 'E':
			print(self.type, self.qubits)
		elif self.type == 'M':
			print(self.type, self.qubit, self.angle, self.X_idxs, self.Z_idxs)
		elif self.type == 'X':
			print(self.type, self.qubit, self.power_idx)
		elif self.type == 'Z':
			print(self.type, self.qubit, self.power_idx)
		






seq = []

#seq.append(Gate('E', [[2,3]]))
#seq.append(Gate('M', [2,0]))
#seq.append(Gate('X', [3,2]))
#seq.append(Gate('E', [[1,3]]))
#seq.append(Gate('E', [[3,4]]))
#seq.append(Gate('M', [3,0]))
#seq.append(Gate('X', [4,3]))
#seq.append(Gate('Z', [5,3]))
#seq.append(Gate('M', [5,np.pi/6]))



#for s in seq:
#	s.printinfo()


qubit_count, gates1, qubits1 = circuit.load('./circuits/circuit1.json')
result = convert(gates1, qubits1, qubit_count)
gates = result['gates']
qubits = result['qubits']
conditions = result['conditions']


for i in range(len(gates)):
	if gates[i]=='E':
		seq.append(Gate('E', [[qubits[0][i], qubits[1][i]]]))
	elif gates[i]=='M':
		seq.append(Gate('M', [qubits[0][i], conditions[i]]))
	elif gates[i] in ('X', 'Y', 'Z'):
		seq.append(Gate(gates[i], [qubits[0][i], conditions[i]]))
	

#print(gates)
#print(np.array(qubits))
#print(conditions)
print('---- in ------')
for s in seq:
	s.printinfo()
print('----- out -----')
#print('------------')


N = len(seq)


i = 1
while i<N:
	#print(i)
	if seq[i].type == 'E':
		if seq[i-1].type == 'E':
			i = i+1
			continue

		if ((seq[i-1].type == 'Z') | ((seq[i].qubits[0] != seq[i-1].qubit) & (seq[i].qubits[1] != seq[i-1].qubit))):
			#print('condition E commute')
			seq[i-1], seq[i] = seq[i], seq[i-1]
			i = i-1
			continue
		elif seq[i-1].type == 'X':
			if seq[i].qubits[0] == seq[i-1].qubit:
				#print('condition 1')
				seq[i-1], seq[i] = seq[i], seq[i-1]
				seq.insert(i, Gate('Z', [seq[i-1].qubits[1],seq[i].power_idx]))
				i = i - 1
				N = len(seq)
				continue
			elif seq[i].qubits[1] == seq[i-1].qubit:
				#print('condition 2')
				seq[i-1], seq[i] = seq[i], seq[i-1]
				seq.insert(i, Gate('Z', [seq[i-1].qubits[0],seq[i].power_idx]))
				i = i - 1
				N = len(seq)
				continue
				
	elif seq[i].type == 'M':
		if ((seq[i-1].type == 'M') | (seq[i-1].type == 'E')):
			i = i+1
			continue
		elif (seq[i].qubit != seq[i-1].qubit):
			#print('condition M commute')
			seq[i-1], seq[i] = seq[i], seq[i-1]
			i = i-1
			continue
		elif (seq[i-1].type == 'X'):
			#print('condition X++')
			seq[i].X_idxs.append(i-1)
			del seq[i-1]
			N = len(seq)
			i = i-1
			continue
		elif (seq[i-1].type == 'Z'):
			#print('condition Z++')
			seq[i].Z_idxs.append(i-1)
			del seq[i-1]
			N = len(seq)
			i = i-1
			continue

		
	i = i+1
	N = len(seq)
	





for s in seq:
	s.printinfo()




			
#print(gates)
#print(np.array(qubits))
#print(conditions)













