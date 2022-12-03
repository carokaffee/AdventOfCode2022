from src.tools.loader import load_data

TESTING = True

def get_score(item):
    if 97 <= ord(item) <= 122:
        return ord(item) - 96
    elif 65 <= ord(item) <= 90:
        return ord(item) - 38
    else:
        raise ValueError('No valid character given')


if __name__ == '__main__':
    data = load_data(TESTING, '\n')

    score_1 = 0
    score_2 = 0
    
    # part 1
    for elfbag in data:
        compartment_1 = set(elfbag[:len(elfbag)//2])
        compartment_2 = set(elfbag[len(elfbag)//2:])
        shared_items = set([item for item in compartment_1 if item in compartment_2])

        for item in shared_items:
            score_1 += get_score(item)

    # part 2
    for i in range(len(data)//3):
        elf_1 = set(data[3*i])
        elf_2 = set(data[3*i+1])
        elf_3 = set(data[3*i+2])
        shared_items_2 = set([item for item in elf_1 if item in elf_2 and item in elf_3])

        for item in shared_items_2:
            score_2 += get_score(item)

# solution 1
print(score_1)

# solution 2
print(score_2)