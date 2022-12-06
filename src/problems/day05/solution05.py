from src.tools.loader import load_data

import copy

TESTING = True

def parse_containers(raw_input):
    number_of_containers = int(raw_input.split()[-1])
    containers = [[] for _ in range(number_of_containers)]
    
    for line in reversed(raw_input.splitlines()[0:-1]):
        for i, letter in enumerate(line[1::4]):
            if letter != ' ':
                containers[i].append(letter)

    return containers


def parse_instructions(raw_input):
    instructions = []
    for line in raw_input.splitlines():
        instructions.append(list(map(int,line.split()[1::2])))
    
    return instructions


if __name__ == '__main__':
    data = load_data(TESTING, '\n\n', strip=False)
    containers_1 = parse_containers(data[0])
    containers_2 = parse_containers(data[0])
    instructions = parse_instructions(data[1])

    for number, start, end in instructions:
        start, end = start - 1, end - 1
        # part 1
        containers_1[end].extend(reversed(containers_1[start][-number:]))
        containers_1[start] = containers_1[start][:-number]
        # part 2
        containers_2[end].extend(containers_2[start][-number:])
        containers_2[start] = containers_2[start][:-number]

    solution_1 = ''
    solution_2 = ''

    for container in containers_1:
        solution_1 += container[-1]

    for container in containers_2:
        solution_2 += container[-1]

    # solution 1
    print(solution_1)

    # solution 2
    print(solution_2)