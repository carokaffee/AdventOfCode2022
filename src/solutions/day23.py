from src.tools.loader import load_data

TESTING = False


def parse_input(data):
    elves = set()
    for i, line in enumerate(data):
        for j, item in enumerate(line):
            if item == "#":
                elves.add((i, j))
    return elves


def is_free(elves, pos, dir):
    x_pos, y_pos = pos
    match dir:
        case 0:  # north
            coords = [(-1, -1), (-1, 0), (-1, 1)]
        case 1:  # south
            coords = [(1, -1), (1, 0), (1, 1)]
        case 2:  # west
            coords = [(-1, -1), (0, -1), (1, -1)]
        case 3:  # east
            coords = [(-1, 1), (0, 1), (1, 1)]

    positions_in_dir = [(x + x_pos, y + y_pos) for x, y in coords]

    if len([c for c in positions_in_dir if c in elves]) == 0:
        return (coords[1][0] + x_pos, coords[1][1] + y_pos)


def get_new_pos(elves, pos, dir_counter):
    free = True
    for i in range(4):
        if not is_free(elves, pos, (dir_counter + i) % 4):
            free = False
    if free:
        return pos

    for i in range(4):
        if new_pos := is_free(elves, pos, (dir_counter + i) % 4):
            return new_pos


def simulate_round(elves):
    global dir_counter
    new_positions = set()
    double_positions = set()
    new_elves = set()

    for elf in elves:
        if new_pos := get_new_pos(elves, elf, dir_counter):
            if new_pos in new_positions:
                double_positions.add(new_pos)
            else:
                new_positions.add(new_pos)

    for elf in elves:
        if new_pos := get_new_pos(elves, elf, dir_counter):
            if new_pos not in double_positions:
                new_elves.add(new_pos)
            else:
                new_elves.add(elf)
        else:
            new_elves.add(elf)

    dir_counter = (dir_counter + 1) % 4

    return new_elves


def simulate_until_done(elves):
    round_counter = 0
    done = False

    while not done:
        round_counter += 1
        new_elves = simulate_round(elves)

        if len([elf for elf in elves if elf in new_elves]) == len(elves):
            done = True

        elves = new_elves

        if round_counter == 10:
            free_positions = get_free_positions(elves)

        if not done:
            print(f"\rSimulating round {round_counter}...", end="")
        else:
            print("\rSimulation finished. No elves move anymore.")

    return elves, round_counter, free_positions


def get_min_max(elves):
    min_x = min([x for x, _ in elves])
    max_x = max([x for x, _ in elves])
    min_y = min([y for _, y in elves])
    max_y = max([y for _, y in elves])
    return min_x, max_x, min_y, max_y


def get_free_positions(elves):
    min_x, max_x, min_y, max_y = get_min_max(elves)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def print_elves_map(elves):
    min_x, max_x, min_y, max_y = get_min_max(elves)

    for i in range(min_x, max_x + 1):
        row = ""
        for j in range(min_y, max_y + 1):
            if (i, j) in elves:
                row += "#"
            else:
                row += "."
        print(row)
    print()


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    elves = parse_input(data)
    dir_counter = 0

    elves, round_counter, free_positions = simulate_until_done(elves)
    print_elves_map(elves)

    # PART 1
    # test:    110
    # answer: 4116
    print("Empty ground tiles after 10 rounds:", free_positions)

    # PART 2
    # test:    20
    # answer: 984
    print("Rounds until no elf moves:", round_counter)
