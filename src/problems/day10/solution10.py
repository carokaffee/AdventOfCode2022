from src.tools.loader import load_data

TESTING = False


def print_screen(input_string):
    for i in range(len(input_string)):
        if (i+1) % 40 == 0:
            print(input_string[(i+1)-40:i])


def parse_input(data):
    cycles = []
    for line in data:
        if line == 'noop':
            cycles.append('hold')
        else:
            cycles.append('hold')
            cycles.append(int(line.split()[1]))
    return cycles


def sum_of_signal_strengths():
    x = 1
    signal_strengths = []

    for i in range(len(cycles)):
        if (i+1) % 40 == 20:
            signal_strengths.append((i+1) * x)
        if cycles[i] != 'hold':
            x += cycles[i]

    return sum(signal_strengths)


def CRT_screen():
    x = 1
    output = ''

    for i in range(len(cycles)):
        output += '#' if i % 40 in [x-1, x, x+1] else '.'
        if cycles[i] != 'hold':
            x += cycles[i]

    return output



if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    cycles = parse_input(data)

    # solution_1
    print(sum_of_signal_strengths())

    # solution_2
    print_screen(CRT_screen())
