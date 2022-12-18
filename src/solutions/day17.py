from src.tools.loader import load_data
from tqdm import tqdm

TESTING = False


def highest_row():
    return len(rows) - 1


def print_tetris():
    for i, row in enumerate(rows[1:][::-1]):
        print(f"{len(rows) - 1 - i}".rjust(4), end=" ")
        print("|" + "".join(row) + "|")
    print("   0 +-------+")


def add_empty_rows(num):
    for _ in range(num):
        rows.append(["."] * 7)


def delete_empty_rows():
    global rows
    while rows[-1] == ["."] * 7:
        rows = rows[:-1]


def transform_to_stone():
    for row in rows:
        for i, item in enumerate(row):
            if item == "@":
                row[i] = "#"


def simulate(step: int):
    match step % 5:
        case 0:
            simulate_minus()
        case 1:
            simulate_plus()
        case 2:
            simulate_el()
        case 3:
            simulate_i()
        case 4:
            simulate_square()

    done = False
    while not done:
        simulate_gust()
        done = simulate_falling()

    transform_to_stone()
    delete_empty_rows()


def simulate_minus():
    global relevant_rows
    add_empty_rows(3)
    rows.append([".", ".", "@", "@", "@", "@", "."])
    relevant_rows = [highest_row()]


def simulate_plus():
    global relevant_rows
    add_empty_rows(3)
    rows.append([".", ".", ".", "@", ".", ".", "."])
    rows.append([".", ".", "@", "@", "@", ".", "."])
    rows.append([".", ".", ".", "@", ".", ".", "."])
    relevant_rows = [highest_row(), highest_row() - 1, highest_row() - 2]


def simulate_el():
    global relevant_rows
    add_empty_rows(3)
    rows.append([".", ".", "@", "@", "@", ".", "."])
    rows.append([".", ".", ".", ".", "@", ".", "."])
    rows.append([".", ".", ".", ".", "@", ".", "."])
    relevant_rows = [highest_row(), highest_row() - 1, highest_row() - 2]


def simulate_i():
    global relevant_rows
    add_empty_rows(3)
    for _ in range(4):
        rows.append([".", ".", "@", ".", ".", ".", "."])
    relevant_rows = [
        highest_row(),
        highest_row() - 1,
        highest_row() - 2,
        highest_row() - 3,
    ]


def simulate_square():
    global relevant_rows
    add_empty_rows(3)
    for _ in range(2):
        rows.append([".", ".", "@", "@", ".", ".", "."])
    relevant_rows = [highest_row(), highest_row() - 1]


def simulate_falling():
    global relevant_rows
    can_fall = True

    for row_num in sorted(relevant_rows):
        for i, item in enumerate(rows[row_num]):
            if item == "@":
                if rows[row_num - 1][i] in ["#", "-"]:
                    can_fall = False

    if can_fall:
        for row_num in sorted(relevant_rows):
            for i, item in enumerate(rows[row_num]):
                if item == "@":
                    rows[row_num - 1][i] = "@"
                    rows[row_num][i] = "."
        relevant_rows = [row - 1 for row in relevant_rows]
        return False

    return True


def simulate_gust() -> bool:
    global gust_iteration
    direction = gusts[gust_iteration % len(gusts)]
    can_move = True

    if direction == ">":
        for row_num in relevant_rows:
            for i, item in enumerate(rows[row_num][::-1]):
                if item == "@":
                    if i == 0 or rows[row_num][6 - (i - 1)] == "#":
                        can_move = False

        if can_move:
            for row_num in relevant_rows:
                for i, item in enumerate(rows[row_num][::-1]):
                    if item == "@":
                        rows[row_num][7 - i] = "@"
                        rows[row_num][6 - i] = "."

    if direction == "<":
        for row_num in relevant_rows:
            for i, item in enumerate(rows[row_num]):
                if item == "@":
                    if i == 0 or rows[row_num][i - 1] == "#":
                        can_move = False

        if can_move:
            for row_num in relevant_rows:
                for i, item in enumerate(rows[row_num]):
                    if item == "@":
                        rows[row_num][i - 1] = "@"
                        rows[row_num][i] = "."

    gust_iteration += 1


def check_if_cycle(iteration):
    go_back = 9
    if len(rows) >= go_back:
        current = [len(rows) - 1, gust_iteration % len(gusts), iteration % 5]
        for i in range(1, go_back):
            current.append(rows[-i])
        cycle_options.append(current)

        for i, elem in enumerate(cycle_options[:-1]):
            if elem[1:] == current[1:]:
                return i, len(cycle_options) - 1


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    gusts = data[0]

    # Part 1
    gust_iteration = 0
    rows = [["-", "-", "-", "-", "-", "-", "-"]]
    relevant_rows = []

    for i in range(2022):
        simulate(i)

    tower_height_small = len(rows) - 1

    # Part 2
    gust_iteration = 0
    rows = [["-", "-", "-", "-", "-", "-", "-"]]
    relevant_rows = []
    heights = []
    cycle_found = False
    cycle_options = []

    for i in tqdm(range(len(gusts) * 2), "search cycle"):
        if not cycle_found:
            cycle_index = check_if_cycle(i)
            if cycle_index is not None:
                cycle_found = True

        simulate(i)
        heights.append(len(rows) - 1)

    cycle_length = cycle_index[1] - cycle_index[0]
    num_of_cycles = 1000000000000 // cycle_length - 1
    height_before = cycle_options[cycle_index[0]][0]
    height_after = cycle_options[cycle_index[1]][0]
    cycle_height = height_after - height_before
    index = 1000000000000 % cycle_length + cycle_length
    last_height = heights[index - 1]

    tower_height_large = num_of_cycles * cycle_height + last_height

    # PART 1
    # test:   3068
    # answer: 3227
    print(tower_height_small)

    # PART 2
    # test:   1514285714288
    # answer: 1597714285698
    print(tower_height_large)
