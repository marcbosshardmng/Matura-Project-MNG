import qcircuits as qc
import numpy as np

database_path = r'C:\Users\marcr\anaconda3\python\database.8.txt'
def load_database(database):
    with open(database, 'r') as file:
        names = [line.strip() for line in file.readlines()]
    return names

def construct_problem(database, target_name):
    num_inputs = len(database)
    answers = np.zeros(num_inputs, dtype=np.int32)


    if target_name in database:
        target_index = database.index(target_name)
        answers[target_index] = 1
    else:
        raise ValueError(f" Fault: Target name'{target_name}' not found in the database.")
    def f(*bits):
        index = sum(v * 2**i for i, v in enumerate(bits))

        return answers[index]

    return f

def grover_algorithm(d, f):
    Oracle = qc.U_f(f, d=d+1)
    H_d = qc.Hadamard(d)
    H = qc.Hadamard()
    N = 2**d
    zero_projector = np.zeros((N, N))
    zero_projector[0, 0] = 1
    Inversion = H_d((2 * qc.Operator.from_matrix(zero_projector) - qc.Identity(d))(H_d))
    Grover = Inversion(Oracle, qubit_indices=range(d))
    state = qc.zeros(d) * qc.ones(1)
    state =(H_d * H)(state)
    angle_to_rotate = np.arccos(np.sqrt(1 / N))
    rotation_angle = 2 * np.arcsin(np.sqrt(1 / N))
    iterations = int(round(angle_to_rotate / rotation_angle))
    for i in range(iterations):
        state = Grover(state)
    measurements = state.measure(qubit_indices=range(d))
    return measurements


if __name__ == '__main__':
    database = load_database(database_path)
    target_name = ("Oliver")
    d = int(np.ceil(np.log2(len(database))))
    f = construct_problem(database, target_name)
    bits = grover_algorithm(d, f)
    print('Measurement: {}'.format(bits))
    print('Evaluate f at measurement: {}'.format(f(*bits)))
    binary_string = ''.join(map(str, bits))
    index = int(binary_string, 2)
    print("Index of the solution:", index)
    print("Name found:", database[index])


