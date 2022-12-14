from src.tools.loader import load_data
import numpy as np

TESTING = True


def parse_input(data):
    corners = []
    stones = set()

    for line in data:
        corners.append([])
        for pair in line.split(' -> '):
            corners[-1].append(np.array(tuple(map(int, pair.split(',')))))
    for line in corners:
        for i in range(len(line)-1):
            direction = line[i+1] - line[i]
            for j in range(int(np.linalg.norm(direction))+1):
                stones.add(tuple(line[i] + j * direction / np.linalg.norm(direction))) 

    return stones
            

def falling_sand():
    global stop_1
    sand_grain = (500, 0)
    while True:
        if sand_grain[1] == lowest_point:
            stop_1 = True
            return

        new_locations = (
            (sand_grain[0], sand_grain[1] + 1),
            (sand_grain[0] - 1, sand_grain[1] + 1),
            (sand_grain[0] + 1, sand_grain[1] + 1)
            )
        blocked = stones.union(sand)

        if new_locations[0] not in blocked:
            sand_grain = new_locations[0]
        elif new_locations[1] not in blocked:
            sand_grain = new_locations[1]
        elif new_locations[2] not in blocked:
            sand_grain = new_locations[2]
        else:
            return sand_grain


def falling_sand_bottom():
    global stop_2
    grain = (500, 0)
    blocked = stones.union(sand2)

    while True:
        new_locations = (
            (grain[0], grain[1] + 1),
            (grain[0] - 1, grain[1] + 1),
            (grain[0] + 1, grain[1] + 1)
            )

        if grain[1] == lowest_point + 1:
            return grain
        elif new_locations[0] not in blocked:
            grain = new_locations[0]
        elif new_locations[1] not in blocked:
            grain = new_locations[1]
        elif new_locations[2] not in blocked:
            grain = new_locations[2]
        elif grain == (500, 0):
            stop_2 = True
            return
        else:
            return grain


if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    stones = parse_input(data)
    sand = set()
    sand2 = set()

    lowest_point = 0
    for stone in stones:
        lowest_point = max(lowest_point, stone[1])

    stop_1 = False
    stop_2 = False

    counter = -1
    counter2 = 0

    while not stop_1:
        counter += 1
        sand.add(falling_sand())

    print(counter)

    while not stop_2:
        counter2 += 1
        sand2.add(falling_sand_bottom())

    print(counter2)

