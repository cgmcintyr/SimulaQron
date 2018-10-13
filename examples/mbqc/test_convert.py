from .aliceTest import convert


def test_convert_h1_has_correct_gates():
    original = { "gates": ["H"], "qubits": [ [1], [0] ], }
    expected_gates = ["E", "M", "X"]
    assert convert(original)["gates"] == expected_gates


def test_convert_h1h2_has_correct_gates():
    original = { "gates": ["H", "H"], "qubits": [ [1, 2], [0, 0] ], }
    expected_gates = ["E", "M", "X", "E", "M", "X"]
    assert convert(original)["gates"] == expected_gates


def test_convert_h1h2_has_correct_qubits():
    original = { "gates": ["H", "H"], "qubits": [ [1, 2], [0, 0] ], }
    expected_qubits = [
        [1,1,3,2,2,4],
        [3,0,0,3,0,0]
    ]
    assert convert(original)["qubits"] == expected_qubits


def test_convert_h2e12h2_has_correct_qubits():
    original = { "gates": ["H", "CZ", "H"], "qubits": [ [2, 1, 2], [0, 2, 0] ], }
    expected_qubits = [
        [2,2,3,1,3,3,4],
        [3,0,0,3,4,0,0]
    ]
    assert convert(original)["qubits"] == expected_qubits
