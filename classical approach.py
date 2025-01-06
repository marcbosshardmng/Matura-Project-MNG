database_path = r'C:\Users\marcr\anaconda3\python\database.4.txt'
def load_database(database):
    with open(database, 'r') as file:
        names = [line.strip() for line in file.readlines()]
    return names
def the_oracle(my_input):
    winner = 'Oliver'
    if my_input == winner:
        return True
    return False
database = load_database(database_path)
found = False
for index, trial_number in enumerate(database):
    print(f"Checking: {trial_number}")
    if the_oracle(trial_number):
        print('Winner found at index %i' % index)
        print('%i calls to the Oracle used' % (index + 1))
        found = True
        break
if not found:
    print("Winner not found in the database.")


