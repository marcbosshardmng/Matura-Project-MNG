import numpy as np
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.quantum_info import Operator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit_aer.noise import NoiseModel, QuantumError, depolarizing_error
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
database_path = r'C:\Users\marcr\anaconda3\python\database.8.txt'
def load_database(database):
    with open(database, 'r') as file:
        names = [line.strip() for line in file.readlines()]
    return names

def create_oracle(target_state):
    n = len(target_state)
    oracle = QuantumCircuit(n)
    for i in range(n):
        if target_state[i] == '0':
            oracle.x(i)
    oracle.h(n-1)
    oracle.mcx(list(range(n-1)), n-1)
    oracle.h(n-1)
    for i in range(n):
        if target_state[i] == '0':
            oracle.x(i)
    return oracle.to_gate()
def apply_diffusion_operator(qc, num_qubits):
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.h(num_qubits - 1)
    qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)
    qc.h(num_qubits - 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))
def grover_search(database, target_name):
    num_qubits = int(np.ceil(np.log2(len(database))))
    print(f"Size of the database: {len(database)}")
    print(f"Number of qubits used: {num_qubits}")
    qc = QuantumCircuit(num_qubits, num_qubits)
    target_index = database.index(target_name)
    target_binary = format(target_index, f'0{num_qubits}b')
    oracle = create_oracle(target_binary)
    qc.h(range(num_qubits))
    iterations = int(np.pi / 4 * np.sqrt(len(database)))
    print(f"Number of iterations: {iterations}")
    for i in range(iterations):
        qc.append(oracle, range(num_qubits))
        apply_diffusion_operator(qc, num_qubits)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc, num_qubits
def run_grover_with_noise(database, target_name, error_rate):
    qc, num_qubits = grover_search(database, target_name)
    noise_model = NoiseModel()
    depol_error_1 = depolarizing_error(error_rate, 1)
    noise_model.add_all_qubit_quantum_error(depol_error_1, ['u1', 'u2', 'u3', 'x', 'h'])
    depol_error_2 = depolarizing_error(error_rate * 2, 2)
    noise_model.add_all_qubit_quantum_error(depol_error_2, ['cx'])
    backend = AerSimulator(noise_model=noise_model)
    transpiled_circuit = transpile(qc, backend)
    result = backend.run(transpiled_circuit, shots=100000).result()
    counts = result.get_counts(qc)
    total_shots = sum(counts.values())
    print("Total number of shots:", total_shots)
    return counts, num_qubits
if __name__ == '__main__':
    database = load_database(database_path)
    target_name = "Oliver"
    base_error_rate = 0.00001
    num_qubits = int(np.ceil(np.log2(len(database))))
    error_rate = base_error_rate *num_qubits
    print(f"\nRunning Grover's algorithm with database size: {len(database)}")
    counts, num_qubits = run_grover_with_noise(database, target_name, error_rate)
    measured_state = max(counts, key=counts.get)
    print('Measurement:', measured_state)
    index = int(measured_state, 2)
    print('Index of the marked state:', index)
    found_name = database[index] if index < len(database) else "Index out of range"
    print('Name found:', found_name)
    print(f'Is the answer correct? {found_name == target_name}')
    print(f'Number of qubits used: {num_qubits}')
    print(f'Number of qubits used: {counts}')
    plot_histogram(counts).show()
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    marked_count = counts.get(measured_state, 0)
    print(f'Count of marked answer "{found_name}": {marked_count}')
    print("Probabilities:", probabilities)
    measured_state = max(counts, key=counts.get)
    index = int(measured_state, 2)
    found_name = database[index] if index < len(database) else "Index out of range"
    print(f'Name found: {found_name}')
    print(f'Is the answer correct? {found_name == target_name}')
    total_shots = sum(counts.values())
