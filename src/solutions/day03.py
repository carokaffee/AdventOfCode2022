from src.tools.loader import load_data

TESTING = False


def get_score(item):
    if 97 <= ord(item) <= 122:
        return ord(item) - 96
    elif 65 <= ord(item) <= 90:
        return ord(item) - 38
    else:
        raise ValueError("No valid character given")


def priority_sum_compartments():
    score = 0

    for elfbag in data:
        bag_1 = set(elfbag[: (len(elfbag) // 2)])
        bag_2 = set(elfbag[(len(elfbag) // 2) :])
        shared_items = bag_1.intersection(bag_2)

        for item in shared_items:
            score += get_score(item)

    return score


def priority_sum_rucksacks():
    score = 0

    for i in range(len(data) // 3):
        elf_1 = set(data[3 * i])
        elf_2 = set(data[3 * i + 1])
        elf_3 = set(data[3 * i + 2])
        shared_items = elf_1.intersection(elf_2).intersection(elf_3)

        for item in shared_items:
            score += get_score(item)

    return score


if __name__ == "__main__":
    data = load_data(TESTING, "\n")

    # PART 1
    # test:    157
    # answer: 7878
    print(priority_sum_compartments())

    # PART 2
    # test:     70
    # answer: 2760
    print(priority_sum_rucksacks())
