from src.tools.loader import load_data

TESTING = False


def shuffle_numbers(numbers, times, multiplier):
    numbers = [num * multiplier for num in numbers]
    modulo = len(numbers)
    shuffled_ids = [i for i in range(modulo)]

    for _ in range(times):
        for id in range(modulo):
            idx = shuffled_ids.index(id)
            shift = numbers[id]
            shuffled_ids.pop(idx)
            shuffled_ids.insert((idx + shift) % (modulo - 1), id)

    zero_id = numbers.index(0)
    zero_pos = shuffled_ids.index(zero_id)
    sum_of_grove_coords = 0

    for i in range(3):
        id = shuffled_ids[(zero_pos + 1000 * (i + 1)) % modulo]
        sum_of_grove_coords += numbers[id]

    return sum_of_grove_coords


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    numbers = list(map(int, data))

    # PART 1
    # test:       3
    # answer: 11123
    print(shuffle_numbers(numbers, 1, 1))

    # PART 2
    # test:      1623178306
    # answer: 4248669215955
    print(shuffle_numbers(numbers, 10, 811589153))
