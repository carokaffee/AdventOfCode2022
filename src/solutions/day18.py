from src.tools.loader import load_data
import numpy as np

TESTING = False


def parse_input(data):
    lava = [(np.array(tuple(map(int, line.split(","))))) for line in data]
    min_dim = min([min(drop) for drop in lava])
    max_dim = max([max(drop) for drop in lava])
    dim = max_dim - min_dim + 3
    grid = np.zeros((dim,) * 3)

    for point in lava:
        grid[tuple(point - np.ones(3, np.int32) * (min_dim - 1))] += 1

    return grid


def is_adjacent(drop1, drop2):
    dist = np.array(drop1) - np.array(drop2)
    if np.linalg.norm(dist) == 1.0:
        return True
    return False


def get_neighbours(point):
    x, y, z = point
    neighbours = [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1),
    ]

    def is_neighbour(point):
        _x, _y, _z = point
        if _x in [-1, dim] or _y in [-1, dim] or _z in [-1, dim]:
            return False
        return True

    return list(filter(is_neighbour, neighbours))


def get_surface_area(grid):
    surface_area = 0
    for point in set(zip(*np.where(grid == 1))):
        for neighbour in get_neighbours(point):
            surface_area += grid[neighbour] == 0

    return surface_area


def get_outside_surface_area(grid):
    active_cubies = [(0, 0, 0)]
    grid[(0, 0, 0)] = 2
    outside_surface = 0

    while active_cubies:
        new_active_cubies = set()
        for active in active_cubies:
            for neighbour in get_neighbours(active):
                if grid[neighbour] == 0:
                    new_active_cubies.add(neighbour)
                    grid[neighbour] = 2
        active_cubies = new_active_cubies

    for point in set(zip(*np.where(grid == 1))):
        for neighbour in get_neighbours(point):
            outside_surface += grid[neighbour] == 2

    return outside_surface


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    lava_grid = parse_input(data)
    dim = lava_grid.shape[0]

    # PART 1
    # test:     64
    # answer: 4456
    print(get_surface_area(lava_grid))

    # PART 2
    # test:      1
    # answer: 2510
    print(get_outside_surface_area(lava_grid))
