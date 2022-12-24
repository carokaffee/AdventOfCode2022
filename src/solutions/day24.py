from src.tools.loader import load_data
import math
import networkx as nx

TESTING = False


def parse_input(data):
    state = set()
    directions = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
    for i, line in enumerate(data):
        for j, elem in enumerate(line):
            if elem in directions.keys():
                state.add((i, j, directions[elem]))
    return state


def move_state(state):
    new_state = set()
    for i, j, (di, dj) in state:
        new_state.add(
            ((i + di - 1) % NUM_ROWS + 1, (j + dj - 1) % NUM_COLS + 1, (di, dj))
        )
    return new_state


def get_free_spots_per_state(state):
    free_spots = set(
        (i, j) for i in range(1, NUM_ROWS + 1) for j in range(1, NUM_COLS + 1)
    )
    for (i, j, _) in state:
        if (i, j) in free_spots:
            free_spots.remove((i, j))

    free_spots.add((0, 1))  # start position
    free_spots.add((NUM_ROWS + 1, NUM_COLS))  # end position

    return free_spots


def get_free_spots(state):
    states = {}
    free_spots = {}

    for i in range(NUM_ITERATIONS + 1):
        states[i] = state
        free_spots[i] = get_free_spots_per_state(state)
        state = move_state(state)

    return free_spots


def find_neighbours(pos, coords):
    x, y = pos
    neighbours = set(
        [(x, y), (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
    ).intersection(coords)
    return neighbours


def initialize_graph(free_spots):
    G = nx.DiGraph()

    for i in range(NUM_ITERATIONS):
        for x, y in free_spots[i]:
            G.add_node((x, y, i))

    for i in range(NUM_ITERATIONS):
        for x, y in free_spots[i]:
            for n_x, n_y in find_neighbours(
                (x, y), free_spots[(i + 1) % NUM_ITERATIONS]
            ):
                G.add_edge((x, y, i), (n_x, n_y, (i + 1) % NUM_ITERATIONS))

    G.add_node("start")
    for i in range(NUM_ITERATIONS):
        G.add_edge((0, 1, i), "start")

    G.add_node("end")
    for i in range(NUM_ITERATIONS):
        G.add_edge((NUM_ROWS + 1, NUM_COLS, i), "end")

    return G


def do_dijkstra(G, node):
    _, _distances = nx.algorithms.dijkstra_predecessor_and_distance(G, node)
    return _distances


def get_length_of_paths(free_spots):
    G = initialize_graph(free_spots)

    distances1 = do_dijkstra(G, (0, 1, 0))
    path_len1 = distances1["end"] - 1

    distances2 = do_dijkstra(G, (NUM_ROWS + 1, NUM_COLS, path_len1 % NUM_ITERATIONS))
    path_len2 = distances2["start"] - 1

    distances3 = do_dijkstra(G, (0, 1, (path_len1 + path_len2) % NUM_ITERATIONS))
    path_len3 = distances3["end"] - 1

    return path_len1, path_len2, path_len3


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    NUM_ROWS = len(data) - 2
    NUM_COLS = len(data[0]) - 2
    NUM_ITERATIONS = math.lcm(NUM_ROWS, NUM_COLS)

    initial_state = parse_input(data)
    free_spots = get_free_spots(initial_state)
    path_len1, path_len2, path_len3 = get_length_of_paths(free_spots)

    # PART 1
    # test:    18
    # answer: 299
    print(path_len1)

    # PART 2
    # test:    54
    # answer: 899
    print(path_len1 + path_len2 + path_len3)
