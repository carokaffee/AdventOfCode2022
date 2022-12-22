from src.tools.loader import load_data
import numpy as np

TESTING = False


def parse_input(data):
    raw_map, inst = data
    rows = raw_map.split("\n")
    np_map = np.zeros((len(rows), max([len(row) for row in rows])))
    for i, row in enumerate(rows):
        for j, item in enumerate(row):
            if item == ".":
                np_map[i, j] = 1
            elif item == "#":
                np_map[i, j] = 2

    return np_map, inst


def get_movements(inst):
    movements = []
    numbers = list(map(int, inst.replace("R", "L").split("L")))
    counter = 0
    num_counter = 0

    for char in inst:
        if char in "LR":
            for _ in range(numbers[num_counter]):
                movements.append(counter % 4)
            counter += 1 if char == "R" else -1
            num_counter += 1

    for _ in range(numbers[-1]):
        movements.append(counter % 4)

    return movements


def cyclic(coord, row_len, col_len):
    row, col = coord
    return np.array((row % row_len, col % col_len))


def jumped(coord, row_len, col_len):
    jumped = False
    row, col = coord
    if row >= row_len or col >= col_len:
        jumped = True
    return jumped


def move_around_map(np_map, movements):
    r, c = np_map.shape
    current_pos = np.array((0, np.argmax(np_map == 1)))

    for move in movements:
        next_pos = current_pos
        while np_map[tuple(cyclic(next_pos + directions[move], r, c))] == 0:
            next_pos = cyclic(next_pos + directions[move], r, c)

        new_pos = cyclic(next_pos + directions[move], r, c)
        if np_map[tuple(new_pos)] == 1:
            current_pos = new_pos

    return current_pos, movements[-1]


def move_around_cube(np_map, movements):
    r, c = np_map.shape
    move_offset = 0
    current_pos = np.array((0, np.argmax(np_map == 1)))

    for move in movements:
        move = (move + move_offset) % 4
        next_pos = current_pos + directions[move]
        next_move = move

        if jumped(next_pos, r, c) or np_map[tuple(next_pos)] == 0:
            next_pos, next_move = get_next_coords_and_dir(current_pos, move)

        if np_map[tuple(next_pos)] == 1:
            current_pos = next_pos
            move_offset += (next_move - move) % 4

    return current_pos, (movements[-1] + move_offset) % 4


def get_next_coords_and_dir(pos, move):
    x, y = pos + np.array((1, 1))
    new_x, new_y = x, y
    new_move = move

    if TESTING:  # I'm so sorry for this function :'D
        if move == 0:
            if 0 < x <= 4:
                new_x = 13 - x
                new_y = 16
                new_move = 2
            elif 4 < x <= 8:
                new_x = 9
                new_y = 21 - x
                new_move = 1
            elif 8 < x <= 12:
                new_x = 13 - x
                new_y = y - 4
                new_move = 2
        elif move == 1:
            if 0 < y <= 4:
                new_x = 12
                new_y = 13 - y
                new_move = 3
            elif 4 < y <= 8:
                new_x = 17 - y
                new_y = 9
                new_move = 0
            elif 8 < y <= 12:
                new_x = 8
                new_y = 13 - y
                new_move = 3
            elif 12 < y <= 16:
                new_x = 21 - y
                new_y = 1
                new_move = 0
        elif move == 2:
            if 0 < x <= 4:
                new_x = 5
                new_y = 4 - x
                new_move = 1
            elif 4 < x <= 8:
                new_x = 12
                new_y = 21 - x
                new_move = 3
            elif 8 < x <= 12:
                new_x = 8
                new_y = 17 - x
                new_move = 3
        elif move == 3:
            if 0 < y <= 4:
                new_x = 1
                new_y = 13 - y
                new_move = 1
            elif 4 < y <= 8:
                new_x = y - 4
                new_y = 9
                new_move = 0
            elif 8 < y <= 12:
                new_x = 5
                new_y = 13 - y
                new_move = 1
            elif 12 < y <= 16:
                new_x = 21 - y
                new_y = 12
                new_move = 2

    else:
        if move == 0:
            if 0 < x <= 50:
                new_x = 151 - x
                new_y = 100
                new_move = 2
            elif 50 < x <= 100:
                new_x = 50
                new_y = 50 + x
                new_move = 3
            elif 100 < x <= 150:
                new_x = 151 - x
                new_y = 150
                new_move = 2
            elif 150 < x <= 200:
                new_x = 150
                new_y = x - 100
                new_move = 3
        elif move == 1:
            if 0 < y <= 50:
                new_x = 1
                new_y = 100 + y
                new_move = 1
            elif 50 < y <= 100:
                new_x = 100 + y
                new_y = 50
                new_move = 2
            elif 100 < y <= 150:
                new_x = y - 50
                new_y = 100
                new_move = 2
        elif move == 2:
            if 0 < x <= 50:
                new_x = 151 - x
                new_y = 1
                new_move = 0
            elif 50 < x <= 100:
                new_x = 101
                new_y = x - 50
                new_move = 1
            elif 100 < x <= 150:
                new_x = 151 - x
                new_y = 51
                new_move = 0
            elif 150 < x <= 200:
                new_x = 1
                new_y = x - 100
                new_move = 1
        elif move == 3:
            if 0 < y <= 50:
                new_x = 50 + y
                new_y = 51
                new_move = 0
            elif 50 < y <= 100:
                new_x = y + 100
                new_y = 1
                new_move = 0
            elif 100 < y <= 150:
                new_x = 200
                new_y = y - 100
                new_move = 3

    return (np.array((new_x - 1, new_y - 1)), new_move)


def get_score(pos, move):
    x, y = pos
    return (x + 1) * 1000 + (y + 1) * 4 + move


if __name__ == "__main__":
    data = load_data(TESTING, "\n\n", strip=False)
    np_map, movements = parse_input(data)
    movements = get_movements(movements)

    directions = (
        np.array((0, 1)),
        np.array((1, 0)),
        np.array((0, -1)),
        np.array((-1, 0)),
    )

    # PART 1
    # test:     6032
    # answer: 189140
    print(get_score(*move_around_map(np_map, movements)))

    # PART 2
    # test:     5031
    # answer: 115063
    print(get_score(*move_around_cube(np_map, movements)))
