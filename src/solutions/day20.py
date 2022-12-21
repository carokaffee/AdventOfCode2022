from src.tools.loader import load_data

TESTING = False


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    numbers = list(map(int, data))

    numbers = [num * 811589153 for num in numbers]

    modulo = len(numbers)
    id_list = [i for i in range(modulo)]
    for _ in range(10):
        for i in range(modulo):
            num_idx = id_list.index(i)
            shift = numbers[i]
            id_list.pop(num_idx)
            id_list.insert((num_idx + shift) % (modulo - 1), i)

    # print(id_list)

    zero_id = numbers.index(0)
    zero_id = id_list.index(zero_id)

    a = id_list[(zero_id + 1000) % modulo]
    a = numbers[a]
    b = id_list[(zero_id + 2000) % modulo]
    b = numbers[b]
    c = id_list[(zero_id + 3000) % modulo]
    c = numbers[c]

    print(a, b, c)
    print(a + b + c)

    """
    # numbers = [(i, numbers[i]) for i in range(len(numbers))]
    modulo = len(numbers)
    id_values = {i: numbers[i] for i in range(modulo)}
    id_position = {i: i for i in range(modulo)}
    id_new_pos = {i: i for i in range(modulo)}

    for id, _ in tqdm(id_position.items()):
        num = numbers[id_new_pos[id]]
        pos = id_new_pos[id]
        if num > 0:
            for i in range(1, num + 1):
                numbers[(pos + i - 1) % modulo], numbers[(pos + i) % modulo] = (
                    numbers[(pos + i) % modulo],
                    numbers[(pos + i - 1) % modulo],
                )
                other_id = [
                    k
                    for k, v in id_values.items()
                    if v == numbers[(pos + i - 1) % modulo]
                ]
                id_new_pos[id] = (id_new_pos[id] + 1) % modulo
                id_new_pos[other_id[0]] = (id_new_pos[other_id[0]] - 1) % modulo
        elif num < 0:
            for i in range(1, abs(num) + 1):
                numbers[(pos - i + 1) % modulo], numbers[(pos - i) % modulo] = (
                    numbers[(pos - i) % modulo],
                    numbers[(pos - i + 1) % modulo],
                )
                other_id = [
                    k
                    for k, v in id_values.items()
                    if v == numbers[(pos - i + 1) % modulo]
                ]
                id_new_pos[id] = (id_new_pos[id] - 1) % modulo
                id_new_pos[other_id[0]] = (id_new_pos[other_id[0]] + 1) % modulo

    pos_zero = [i for i in range(modulo) if numbers[i] == 0][0]
    a = numbers[(pos_zero + 1000) % modulo]
    b = numbers[(pos_zero + 2000) % modulo]
    c = numbers[(pos_zero + 3000) % modulo]
    print(a, b, c)
    print(a + b + c)
    """
