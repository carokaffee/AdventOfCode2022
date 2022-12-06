from src.tools.loader import load_data

TESTING = True

def parse_sections(line):
    elves = [tuple(map(int, item.split('-'))) for item in line.split(',')]
    elf_1 = set(range(elves[0][0], elves[0][1]+1))
    elf_2 = set(range(elves[1][0], elves[1][1]+1))
    return elf_1, elf_2


if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    subset_counter = 0
    overlap_counter = 0

    for line in data:
        section_1, section_2 = parse_sections(line)
        # part 1
        if section_1.issubset(section_2) or section_2.issubset(section_1):
            subset_counter += 1
        # part 2
        if section_1.intersection(section_2):
            overlap_counter += 1
    
    # solution 1
    print(subset_counter)

    # solution_2
    print(overlap_counter)