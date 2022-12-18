from src.tools.loader import load_data
import numpy as np

TESTING = False


def parse_input(data):
    corners = []
    stones = set()

    for line in data:
        corners.append([])
        for pair in line.split(" -> "):
            corners[-1].append(np.array(tuple(map(int, pair.split(",")))))
    for line in corners:
        for i in range(len(line) - 1):
            direction = line[i + 1] - line[i]
            for j in range(int(np.linalg.norm(direction)) + 1):
                stones.add(tuple(line[i] + j * direction / np.linalg.norm(direction)))

    return stones


def simulate_sand_unit(sand, bottom):
    grain = (500, 0)
    blocked = stones.union(sand)

    while True:
        new_locations = (
            (grain[0], grain[1] + 1),
            (grain[0] - 1, grain[1] + 1),
            (grain[0] + 1, grain[1] + 1),
        )

        if not bottom and grain[1] == lowest_point:
            return
        elif bottom and grain[1] == lowest_point + 1:
            return grain
        elif new_locations[0] not in blocked:
            grain = new_locations[0]
        elif new_locations[1] not in blocked:
            grain = new_locations[1]
        elif new_locations[2] not in blocked:
            grain = new_locations[2]
        elif grain == (500, 0):
            return
        else:
            return grain


def simulate_sand(bottom):
    sand = set()

    while grain := simulate_sand_unit(sand, bottom):
        sand.add(grain)

    return len(sand) + bottom


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    stones = parse_input(data)

    lowest_point = 0
    for stone in stones:
        lowest_point = max(lowest_point, stone[1])

    # PART 1
    # test:     24
    # answer: 1513
    print(simulate_sand(bottom=False))

    # PART 2
    # test:      93
    # answer: 22646
    print(simulate_sand(bottom=True))
