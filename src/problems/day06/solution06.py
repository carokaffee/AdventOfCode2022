from src.tools.loader import load_data

TESTING = True

if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    datastream = data[0]

    solution_1, solution_2 = 0, 0
    
    for i, character in enumerate(datastream):
        if len(set(datastream[i:i+4])) == 4:
            solution_1 = i + 4
            break
    
    for i, character in enumerate(datastream):
        if len(set(datastream[i:i+14])) == 14:
            solution_2 = i + 14
            break

    # solution_1
    print(solution_1)

    # solution_2
    print(solution_2)