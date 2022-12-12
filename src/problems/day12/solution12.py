from src.tools.loader import load_data
import numpy as np

TESTING = True


def parse_input(data):
    heights = []
    for x, line in enumerate(data):
        heights.append([])    
        for y, letter in enumerate(line):
            if letter == 'S':
                heights[x].append(1)
                start = (x,y)
            elif letter == 'E':
                heights[x].append(26)
                end = (x,y)
            else:
                heights[x].append(ord(letter) - 96)
    
    return np.array(heights), start, end


def get_neighbours(x, y, heights):
    neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    def is_neighbour(point):
        _x, _y = point
        if _x in [-1, num_rows] or _y in [-1, num_cols]:
            return False
        if heights[_x, _y] > heights[x, y] + 1:
            return False
        return True

    return list(filter(is_neighbour, neighbours))


def do_dijkstra(heights, start):

    distances = {(x,y) : 2**20 for x in range(num_rows) for y in range(num_cols)}
    current_points = {start}
    distances[start] = 0

    while len(current_points) > 0:
        x, y = min(current_points, key=lambda p: distances[p])
        current_points.remove((x,y))
        neighbours = get_neighbours(x, y, heights)

        for neigh_x, neigh_y in neighbours:
            if distances[(neigh_x, neigh_y)] > distances[(x,y)] + 1:
                distances[(neigh_x, neigh_y)] = distances[(x,y)] + 1
                current_points.add((neigh_x, neigh_y))

    return distances



if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    heights, start, end = parse_input(data)
    num_rows, num_cols = heights.shape

    # part 1
    distances = do_dijkstra(heights, start)
    print(distances[end])

    # part 2
    distances = do_dijkstra(-heights, end)
    print(min([distances[p] for p in distances.keys() if heights[p] == 1]))
