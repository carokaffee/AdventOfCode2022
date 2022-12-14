from src.tools.loader import load_data
import numpy as np

TESTING = False


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
    sand_grain = (500, 0)
    while True:
        if sand_grain[1] == lowest_point:
            return False
        new_locations = (
            (sand_grain[0], sand_grain[1] + 1),
            (sand_grain[0] - 1, sand_grain[1] + 1),
            (sand_grain[0] + 1, sand_grain[1] + 1)
            )
        if new_locations[0] not in stones.union(sand):
            sand_grain = new_locations[0]
        elif new_locations[1] not in stones.union(sand):
            sand_grain = new_locations[1]
        elif new_locations[2] not in stones.union(sand):
            sand_grain = new_locations[2]
        else:
            return sand_grain


if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    stones = parse_input(data)
    sand = set()

    lowest_point = 0
    for stone in stones:
        lowest_point = max(lowest_point, stone[1])
    print(lowest_point)

    counter = 0
    print(sand)

    while falling_sand():
        counter += 1
        sand.add(falling_sand())
        print(len(sand))
        print(counter)

    print(counter)

