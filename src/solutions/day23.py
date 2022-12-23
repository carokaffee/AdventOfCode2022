from src.tools.loader import load_data
import numpy as np

TESTING = True


def parse_input(data):
    elves = []
    for i, line in enumerate(data):
        for j, item in enumerate(line):
            if item == "#":
                elves.append((i, j))
    return elves


def print_elves_map(elves):
    min_x = min([x for x, _ in elves])
    max_x = max([x for x, _ in elves])
    min_y = min([y for _, y in elves])
    max_y = max([y for _, y in elves])
    for i in range(min_x, max_x + 1):
        row = ""
        for j in range(min_y, max_y + 1):
            if (i, j) in elves:
                row += "#"
            else:
                row += "."
        print(row)
    print()


def is_free(elves, pos, dir):
    match dir:
        case 0:  # north
            coords = [(-1, -1), (-1, 0), (-1, 1)]
        case 1:  # south
            coords = [(1, -1), (1, 0), (1, 1)]
        case 2:  # west
            coords = [(-1, -1), (0, -1), (1, -1)]
        case 3:  # east
            coords = [(-1, 1), (0, 1), (1, 1)]

    new_pos = [tuple(np.array(pos) + np.array(coord)) for coord in coords]
    if len([c for c in new_pos if c in elves]) == 0:
        return tuple(np.array(pos) + np.array(coords[1]))


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
    new_positions = []
    new_elves = []
    for elf in elves:
        if new_pos := get_new_pos(elves, elf, dir_counter):
            new_positions.append(new_pos)

    for elf in elves:
        if new_pos := get_new_pos(elves, elf, dir_counter):
            if new_positions.count(new_pos) == 1:
                new_elves.append(new_pos)
            else:
                new_elves.append(elf)
        else:
            new_elves.append(elf)

    dir_counter = (dir_counter + 1) % 4

    return new_elves


def get_free_positions(elves):
    min_x = min([x for x, _ in elves])
    max_x = max([x for x, _ in elves])
    min_y = min([y for _, y in elves])
    max_y = max([y for _, y in elves])
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    elves = parse_input(data)
    dir_counter = 0

    print_elves_map(elves)
    done = False
    round_counter = 0
    while not done:
        round_counter += 1
        new_elves = simulate_round(elves)
        if len([elf for elf in elves if elf in new_elves]) == len(elves):
            print_elves_map(elves)
            print(f"Done after {round_counter} rounds")
            done = True
        elves = new_elves

    print(get_free_positions(elves))
