from src.tools.loader import load_data

TESTING = False


def parse_containers(raw_input):
    number_of_containers = int(raw_input.split()[-1])
    containers = [[] for _ in range(number_of_containers)]

    for line in reversed(raw_input.splitlines()[0:-1]):
        for i, letter in enumerate(line[1::4]):
            if letter != " ":
                containers[i].append(letter)

    return containers


def parse_instructions(raw_input):
    instructions = []
    for line in raw_input.splitlines():
        instructions.append(list(map(int, line.split()[1::2])))

    return instructions


def do_instructions(move_chunks):
    containers = parse_containers(data[0])
    instructions = parse_instructions(data[1])

    for number, start, end in instructions:
        start, end = start - 1, end - 1
        if move_chunks:
            containers[end].extend(containers[start][-number:])
        else:
            containers[end].extend(reversed(containers[start][-number:]))

        containers[start] = containers[start][:-number]

    top_crates = ""

    for container in containers:
        top_crates += container[-1]

    return top_crates


if __name__ == "__main__":
    data = load_data(TESTING, "\n\n", strip=False)

    # PART 1
    # test:   CMZ
    # answer: MQSHJMWNH
    print(do_instructions(move_chunks=False))

    # PART 2
    # test:   MCD
    # answer: LLWJRBHVZ
    print(do_instructions(move_chunks=True))
