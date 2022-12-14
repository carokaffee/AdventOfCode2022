from src.tools.loader import load_data
import copy

TESTING = False


def parse_input(data):
    monkeys = []
    items = {}
    operation = {}
    modulo = {}
    action = {}

    for chunk in data:
        lines = [line.strip() for line in chunk.split("\n")]
        monkey = int(lines[0].split()[1][:-1])
        monkeys.append(monkey)
        items[monkey] = list(map(int, lines[1].split(": ")[1].split(", ")))
        operation[monkey] = eval(
            "lambda old: " + lines[2].split(": ")[1].split(" = ")[1]
        )
        modulo[monkey] = int(lines[3].split()[-1])
        action[monkey] = {
            True: int(lines[4].split()[-1]),
            False: int(lines[5].split()[-1]),
        }

    return monkeys, items, operation, modulo, action


def most_inspections_with_relief(num_of_rounds):
    inspections = [0 for _ in monkeys]
    current_items = copy.deepcopy(items)

    for _ in range(num_of_rounds):
        current_items, inspections = do_round_with_relief(current_items, inspections)

    return list(sorted(inspections))[-2:]


def do_round_with_relief(items, inspections):
    for monkey in monkeys:
        inspections[monkey] += len(items[monkey])

        for item in items[monkey]:
            worry_level = operation[monkey](item) // 3
            next_monkey = action[monkey][worry_level % modulo[monkey] == 0]
            items[next_monkey].append(worry_level)

        items[monkey] = []

    return items, inspections


def most_inspections_with_mod(num_of_rounds):
    inspections = [0 for _ in monkeys]
    current_items = copy.deepcopy(items)

    for monkey, item_list in current_items.items():
        for i, item in enumerate(item_list):
            current_items[monkey][i] = {m: item for m in monkeys}

    for _ in range(num_of_rounds):
        current_items, inspections = do_round_with_mod(current_items, inspections)

    return list(sorted(inspections))[-2:]


def do_round_with_mod(items, inspections):
    for monkey in monkeys:
        inspections[monkey] += len(items[monkey])

        for item_mod_monkeys in items[monkey]:
            item_mod_monkeys.update(
                {
                    m: operation[monkey](item) % modulo[m]
                    for m, item in item_mod_monkeys.items()
                }
            )
            next_monkey = action[monkey][item_mod_monkeys[monkey] % modulo[monkey] == 0]
            items[next_monkey].append(item_mod_monkeys)

        items[monkey] = []

    return items, inspections


if __name__ == "__main__":
    data = load_data(TESTING, "\n\n")
    monkeys, items, operation, modulo, action = parse_input(data)

    # PART 1
    # test:    10605
    # answer: 112221
    a, b = most_inspections_with_relief(20)
    print(a * b)

    # PART 2
    # test:    2713310158
    # answer: 25272176808
    a, b = most_inspections_with_mod(10000)
    print(a * b)
