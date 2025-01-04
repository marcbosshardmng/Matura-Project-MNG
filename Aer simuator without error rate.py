import numpy as np
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit import transpile
from qiskit.quantum_info import Operator
from qiskit.visualization import plot_histogram
import random
from itertools import product
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
database_path = r'C:\Users\marcr\anaconda3\python\database.16.txt'
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
    oracle.h(n - 1)
    oracle.mcx(list(range(n - 1)), n - 1)
    oracle.h(n - 1)
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
    print(num_qubits)
    qc = QuantumCircuit(num_qubits, num_qubits)
    target_index = database.index(target_name)
    target_binary = format(target_index, f'0{num_qubits}b')
    oracle = create_oracle(target_binary)
    qc.h(range(num_qubits))
    iterations = int(np.pi / 4 * np.sqrt(len(database)))
    for i in range(iterations):
        qc.append(oracle, range(num_qubits))
        apply_diffusion_operator(qc, num_qubits)
    qc.measure(range(num_qubits), range(num_qubits))
    return qc

if __name__ == '__main__':
    database = load_database(database_path)
    target_name = "Oliver"
    print(f"Searching for the name: {target_name}")
    qc = grover_search(database, target_name)
    backend = Aer.get_backend('aer_simulator')
    transpiled_circuit = transpile(qc, backend)
    result = backend.run(transpiled_circuit, shots=1000000).result()
    counts = result.get_counts(qc)
    num_unique_states = len(counts)
    print(f"Number of unique measured states: {num_unique_states}")
    measured_state = max(counts, key=counts.get)
    print('Measurement:', measured_state)
    index = int(measured_state, 2)
    print('Index of the marked state:', index)
    found_name = database[index] if index < len(database) else "Index out of range"
    print('Name found:', found_name)
    print(f'Is the answer correct? {found_name == target_name}')
    num_qubits = int(np.ceil(np.log2(len(database))))
    print(f'Number of qubits used: {num_qubits}')
    plot_histogram(counts).show()

    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    marked_count = counts.get(measured_state, 0)
    print(f'Count of marked answer "{found_name}": {marked_count}')
    print("Probabilities:", probabilities)
    fig = plot_histogram(probabilities)
    ax = fig.get_axes()[0]
    plt.rcParams['figure.dpi'] = 400
    ax.set_xlabel('Quantum States')
    ax.set_ylabel('Probability' )
    ax.set_title('Measurement outcomes from Grover\'s search algorithm', fontsize=8)
    plt.xticks(rotation=70)
    plt.show()




