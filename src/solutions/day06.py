from src.tools.loader import load_data

TESTING = False


def start_of_message_marker(length):
    position = 0

    for i in range(len(datastream)):
        if len(set(datastream[i : i + length])) == length:
            position = i + length
            break

    return position


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    datastream = data[0]

    # PART 1
    # test:     11
    # answer: 1282
    print(start_of_message_marker(4))

    # PART 2
    # test:     26
    # answer: 3513
    print(start_of_message_marker(14))
