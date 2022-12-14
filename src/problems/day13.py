from src.tools.loader import load_data
from more_itertools import chunked

TESTING = False


def parse_input(data):
    result = []
    for pair in data:
        a, b = pair.split("\n")
        for p in a + b:
            assert p in [  # safety first
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "[",
                "]",
                ",",
                " ",
            ]
        result.append(eval(a))
        result.append(eval(b))
    return result


def compare_integers(a, b):
    if a != b:
        return a < b


def compare_lists(a, b):
    for el1, el2 in zip(a, b):
        comparison = is_in_right_order(el1, el2)
        if comparison is not None:
            return comparison

    if len(a) != len(b):
        return len(a) < len(b)


def is_in_right_order(a, b):
    if type(a) == int and type(b) == int:
        return compare_integers(a, b)
    elif type(a) == int and type(b) == list:
        return compare_lists([a], b)
    elif type(a) == list and type(b) == int:
        return compare_lists(a, [b])
    else:
        return compare_lists(a, b)


def sum_of_ordered_pair_indices(signals):
    correct_indices = []

    for i, (a, b) in enumerate(chunked(signals, 2)):
        if is_in_right_order(a, b):
            correct_indices.append(i + 1)

    return sum(correct_indices)


def find_decoder_key(signals):
    signals.append([[2]])
    signals.append([[6]])

    # Bubble sort! oOoOo8o8Oo
    for _ in range(len(signals)):
        for i in range(len(signals) - 1):
            if not is_in_right_order(signals[i], signals[i + 1]):
                signals[i], signals[i + 1] = signals[i + 1], signals[i]

    a = signals.index([[2]]) + 1
    b = signals.index([[6]]) + 1

    return a * b


if __name__ == "__main__":
    data = load_data(TESTING, "\n\n")
    signals = parse_input(data)

    # PART 1
    # test:     13
    # answer: 4894
    print(sum_of_ordered_pair_indices(signals))

    # PART 2
    # test:     140
    # answer: 24180
    print(find_decoder_key(signals))
