from src.tools.loader import load_data

TESTING = False


if __name__ == "__main__":
    data = load_data(TESTING, "\n\n")
    data = [list(map(int, item.split("\n"))) for item in data]
    elves = list(map(sum, data))

    # PART 1
    # test:   24000
    # answer: 69795
    print(max(elves))

    # PART 2
    # test:    45000
    # answer: 208437
    print(sum(sorted(elves)[-3:]))
