from src.tools.loader import load_data
from sympy import symbols, Eq, solveset

TESTING = False


def parse_input(data):
    operations = {}
    numbers = {}

    for line in data:
        monkey, expression = line.split(": ")
        if " " in expression:
            name1, op, name2 = expression.split()
            operations[monkey] = (name1, op, name2)
        else:
            numbers[monkey] = int(expression)

    return operations, numbers


def get_root_number():
    operations, numbers = parse_input(data)

    while operations:
        new_monkeys_done = set()

        for monkey, (num1, op, num2) in operations.items():
            if {num1, num2}.issubset(numbers.keys()):
                new_monkeys_done.add(monkey)
                numbers[monkey] = int(
                    eval(f"{numbers[num1]}" + op + f"{numbers[num2]}")
                )

        for new_monkey in new_monkeys_done:
            operations.pop(new_monkey)

    return numbers["root"]


def both_sides_equal_at():
    operations, numbers = parse_input(data)
    numbers.pop("humn")
    name1, _, name2 = operations["root"]

    def create_term(name):
        all_monkeys = operations.keys() | numbers.keys()
        while (involved_monkeys := [m for m in all_monkeys if m in name]) not in [
            ["humn"],
            [],
        ]:
            for monkey in involved_monkeys:
                if monkey in numbers.keys():
                    name = name.replace(monkey, f"{numbers[monkey]}")
                else:
                    name = name.replace(
                        monkey,
                        f"({operations[monkey][0]} {operations[monkey][1]} {operations[monkey][2]})",
                    )
        return name

    name1 = create_term(name1)
    name2 = create_term(name2)

    humn = symbols("humn")
    lhs = eval(f"{name1}", {}, {"humn": humn})
    rhs = eval(f"{name2}", {}, {"humn": humn})

    return int(list(solveset(Eq(lhs, rhs), humn))[0])


if __name__ == "__main__":
    data = load_data(TESTING, "\n")

    # PART 1
    # test:              152
    # answer: 93813115694560
    print(get_root_number())

    # PART 2
    # test:             301
    # answer: 3910938071092
    print(both_sides_equal_at())
