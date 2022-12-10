from src.tools.loader import load_data
import numpy as np

TESTING = True


def parse_input(data):
    movements = []
    for line in data:
        move, num = line.split()
        for _ in range(int(num)):
            movements.append(move)
    return movements


def move_head(move, head):
    match move:
        case 'R':
            head[0] += 1
        case 'L':
            head[0] -= 1
        case 'D':
            head[1] -= 1
        case 'U':
            head[1] += 1
    return head


def move_tail(head, tail):
    distance = head - tail

    if np.linalg.norm(distance) > 1.5:
        if np.abs(distance[0]) > 0:
            tail[0] += np.sign(distance[0])
        if np.abs(distance[1]) > 0:
            tail[1] += np.sign(distance[1])

    return tail


def visited_by_end_of_rope(length):
    rope = [np.zeros((2,)) for _ in range(length)]
    visited = set()

    for move in movements:
        rope[0] = move_head(move, rope[0])

        for i in range(length-1):
            rope[i+1] = move_tail(rope[i], rope[i+1])

        visited.add(tuple(rope[-1]))

    return len(visited)



if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    movements = parse_input(data)

    # solution 1
    print(visited_by_end_of_rope(2))

    # solution 2
    print(visited_by_end_of_rope(10))