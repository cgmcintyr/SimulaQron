import sys
import json
from SimulaQron.cqc.pythonLib.cqc import CQCConnection, CQCNoQubitError

num_qubits = 4
qubits = []
num_measurements


with CQCConnection("server") as Server:

	for i in range(num_qubits):
		qubits.append(Server.recvQbit())

	pairs_to_entangle = Server.recvClassical()

	for p in pairs_to_entangle:
		qubits[p[0]].CNOT(p[1])

	for i in range(num_measurements):
		idx, angle = Server.recvClassical()
		qubits[idx].rot_Z(angle)
		m = qubits[idx].measure()
		Server.sendClassical('client', m)




'''
		run = 0
		while run < nr_runs:

			try:
				# Create an EPR pair
				q = Alice.createEPR("Bob")
			except CQCNoQubitError:
				continue

			run += 1

			# Get the identifier of this EPR pair such that we can relate our measurement outcomes to Bobs
			sequence_nr = q.get_entInfo().id_AB

			print("Generated EPR pair number {}.".format(sequence_nr))

			if (sequence_nr % 3) == 0:
				# Measure in Z
				basis = 'Z'
			elif (sequence_nr % 3) == 1:
				# Measure in X
				q.H()
				basis = 'X'
			else:
				# Measure in Y
				q.K()
				basis = 'Y'

			m = q.measure()
			# We save both the measurement outcome and the measurement basis
			meas_outcomes[sequence_nr] = (m, basis)

	# Get the measurement outcomes from Bob
	msg = Alice.recvClassical(msg_size=10000)

	# Decode the message
	bob_meas_outcomes = json.loads(msg.decode('utf-8'))

	# Check the measurement outcomes
	errors = []
	for (sequence_nr, mB) in bob_meas_outcomes.items():
		mA, basis = meas_outcomes[int(sequence_nr)]
		if basis == 'Y':
			if mA == mB:  # In a noiseless situation this shouldn't happen
				errors.append(True)
			else:
				errors.append(False)
		else:
			if mA != mB:  # In a noiseless situation this shouldn't happen
				errors.append(True)
			else:
				errors.append(False)

	nr_data_points = len(errors)
	avg_QBER = errors.count(True) / nr_data_points
	to_print="Estimated QBER is {} (from {} data-points.".format(avg_QBER, nr_data_points)
	print("|"+"-"*(len(to_print)+2)+"|")
	print("| "+to_print+" |")
	print("|"+"-"*(len(to_print)+2)+"|")

if __name__ == '__main__':
	try:
		nr_runs = int(sys.argv[1])
	except Exception:
		nr_runs = 500
	if nr_runs > 1000:
		raise ValueError("Number of EPR pairs for this example is currently restricted to less than 1000")
	main(nr_runs)
