import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService
import qiskit_ibm_runtime
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel="ibm_quantum")
QiskitRuntimeService.save_account(
    channel="ibm_quantum",
    token="API Token",#Here was my API-token which I took from the IBM quantum cloud.After login into the cloud, the API-token is on the top left hand side
    overwrite=True
)

import matplotlib.pyplot as plt
database_path = r'C:\Users\marcr\anaconda3\python\database.4.txt'
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
    return oracle.to_gate(label="Oracle")

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
    print(f"Number of qubits: {num_qubits}")
    qc = QuantumCircuit(num_qubits, num_qubits)
    target_index = database.index(target_name)
    target_binary = format(target_index, f'0{num_qubits}b')
    oracle = create_oracle(target_binary)
    qc.h(range(num_qubits))
    iterations = int(np.pi / 4 * np.sqrt(len(database)))
    print(f"Iterations: {iterations}")
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
    backend = service.backend('ibm_brisbane')
    transpiled_circuit = transpile(qc, backend, optimization_level=3)
    print("Running on the real quantum backend...")
    job = backend.run(transpiled_circuit, shots=100000)
    print("Job submitted. Waiting for results...")
    result = job.result()
    counts_dict = result.get_counts()
    measured_state = max(counts_dict, key=counts_dict.get)
    print('Measurement:', measured_state)
    try:
        index = int(measured_state, 2)  # Convert binary string to integer
        print('Index of the marked state:', index)
        found_name = database[index] if index < len(database) else "Index out of range"
        print('Name found:', found_name)
        print(f'Is the answer correct? {found_name == target_name}')

        num_qubits = int(np.ceil(np.log2(len(database))))

        total_shots = sum(counts_dict.values())
        probabilities = {state: count / total_shots for state, count in counts_dict.items()}
        print("Probabilities:", probabilities)
        marked_count = counts_dict.get(measured_state, 0)
        print(f'Count of marked answer "{found_name}": {marked_count}')
        print("Counts for each state:")
        for state, count in counts_dict.items():  # Iterating over items in counts_dict
            print(f"State: {state}, Count: {count}")
    except ValueError as e:
            print(f"Error converting measured state to index: {e}")
