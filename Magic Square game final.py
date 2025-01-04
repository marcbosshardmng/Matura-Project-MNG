import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator
import random

def define_initial_state():
    psi = np.zeros(16, dtype=complex)
    psi[3]  =  +0.5
    psi[6]  =  -0.5
    psi[9]  =  -0.5
    psi[12] =  +0.5
    return psi

def define_unitary_operators():
    A1_matrix = (1 / np.sqrt(2)) * np.array([
       [1j,  0,   0,   1 ],
       [0,  -1j,  1,   0 ],
       [0,   1j,  1,   0 ],
       [1,   0,   0,  1j]
    ], dtype=complex)

    A2_matrix = (1 / 2)* np.array([
       [ 1j,   1,   1,   1j],
       [-1j,   1,  -1,   1j],
       [ 1j,   1,  -1,  -1j],
       [-1j,   1,   1,  -1j]
    ], dtype=complex)

    A3_matrix = (1 / 2)* np.array([
       [-1,  -1,  -1,   1],
       [ 1,   1,  -1,   1],
       [ 1,  -1,   1,   1],
       [ 1,  -1,  -1,  -1]
    ], dtype=complex)

    B1_matrix = (1 / 2)* np.array([
       [ 1j,  -1j,  1,   1],
       [-1j,  -1j,  1,  -1],
       [ 1,    1,  -1j,  1j],
       [-1j,   1j,  1,   1]
    ], dtype=complex)

    B2_matrix = (1 / 2)* np.array([
       [-1,   1j,  1,   1j],
       [ 1,    1j,  1,  -1j],
       [ 1,   -1j,  1,   1j],
       [-1,  -1j,  1,  -1j]
    ], dtype=complex)

    B3_matrix = (1 / np.sqrt(2)) * np.array([
       [ 1,  0,  0,  1],
       [-1,  0,  0,  1],
       [ 0,  1,  1,  0],
       [ 0,  1, -1,  0]
    ], dtype=complex)

    operators = {
        'A1': Operator(A1_matrix),
        'A2': Operator(A2_matrix),
        'A3': Operator(A3_matrix),
        'B1': Operator(B1_matrix),
        'B2': Operator(B2_matrix),
        'B3': Operator(B3_matrix)
    }
    return operators

def create_quantum_circuit(psi, operators, x, y):
    qc = QuantumCircuit(4, 4)
    qc.initialize(psi, [0, 1, 2, 3])
    if x == 1:
        qc.unitary(operators['A1'], [0, 1], label='A1')
    elif x == 2:
        qc.unitary(operators['A2'], [0, 1], label='A2')
    elif x == 3:
        qc.unitary(operators['A3'], [0, 1], label='A3')

    if y == 1:
        qc.unitary(operators['B1'], [2, 3], label='B1')
    elif y == 2:
        qc.unitary(operators['B2'], [2, 3], label='B2')
    elif y == 3:
        qc.unitary(operators['B3'], [2, 3], label='B3')
    qc.measure([0, 1, 2, 3], [0, 1, 2, 3])
    return qc

def execute_circuit(qc, shots=1000000):
    backend = AerSimulator()
    job = backend.run(transpile(qc, backend), shots=shots)
    result = job.result()
    counts = result.get_counts()
    print(f"Measurement Outcomes: {counts}")
    return counts

def interpret_magic_square(counts, x, y):
    wins = 0
    losses = 0
    for outcome_str, freq in counts.items():
        q0 = int(outcome_str[3])
        q1 = int(outcome_str[2])
        q2 = int(outcome_str[1])
        q3 = int(outcome_str[0])
        a3 = 0
        if q0 == 0 and q1 == 0:
            a3 = 1
        if q0 == 1 and q1 == 0:
            a3 = 0
        if q0 == 0 and q1 == 1:
            a3 = 0
        if q0 == 1 and q1 == 1:
            a3 = 1

        b3 = 0
        if q2 == 0 and q3 == 0:
            b3 = 0
        if q2 == 1 and q3 == 0:
            b3 = 1
        if q2 == 0 and q3 == 1:
            b3 = 1
        if q2 == 1 and q3 == 1:
            b3 = 0

        if x == 1:
            a = q0
        elif x == 2:
            a = q1
        else:
            a = a3

        if y == 1:
            b = q2
        elif y == 2:
            b = q3
        else:
            b = b3
    if a == b:
        wins += freq
    else:
        losses += freq
    return wins, losses

def run_all_xy(psi, operators, shots):
    total_wins = 0
    total_losses = 0
    for x in [1, 2, 3]:
        for y in [1, 2, 3]:
            qc = create_quantum_circuit(psi, operators, x, y)
            counts = execute_circuit(qc, shots=shots)
            wins, losses = interpret_magic_square(counts, x, y)
            total_wins += wins
            total_losses += losses
            pair_total = wins + losses
            pair_frac = wins / pair_total if pair_total else 0
            print(f"(x={x}, y={y}): wins={wins}, losses={losses}, total={pair_total}, fraction={pair_frac:.3f}")
    overall = total_wins + total_losses
    frac = total_wins / overall if overall else 0.0
    print("\n=== Magic Square Overall ===")
    print(f"  total wins   = {total_wins}")
    print(f"  total losses = {total_losses}")
    print(f"  total shots  = {overall}")
    print(f"  win fraction = {frac:.3f}")
    return total_wins, total_losses

def main():
    total_wins = 0
    total_losses = 0
    num_iterations = 5
    win_rates = []
    for iteration in range(num_iterations):
        print(f"\nIteration {iteration + 1} ")
        psi = define_initial_state()
        operators = define_unitary_operators()
        wins, losses = run_all_xy(psi, operators, shots=10000)
        total_wins += wins
        total_losses += losses
        win_rate = wins / (wins + losses) if (wins + losses) > 0 else 0
        win_rates.append(win_rate)
        print(f"Iteration {iteration + 1}: Wins = {wins}, Losses = {losses}")
    average_win_rate = sum(win_rates) / num_iterations if num_iterations > 0 else 0
    print(f"\nAverage Win Rate over {num_iterations} iterations: {average_win_rate:.3f}")
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, num_iterations + 1), win_rates, marker='o', linestyle='-', label='Win Rate')
    plt.xlabel('Iteration')
    plt.ylabel('Win Rate')
    plt.grid()
    plt.legend()
    plt.show()
    print(f"Final Results After {num_iterations}  Iterations")
    print(f"Total Wins   = {total_wins}")
    print(f"Total Losses = {total_losses}")
    print(f"Final Win Rate = {total_wins / (total_wins + total_losses):.3f}")
if __name__ == "__main__":
    main()
