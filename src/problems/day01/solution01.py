from src.tools.loader import load_data

TESTING = True

if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    elves = [0]
    counter = 0
    for item in data:
        if item == '':
            elves.append(0)
            counter += 1
            continue
        item = int(item)
        elves[counter] += item
    print(max(elves))
    print(sum(sorted(elves)[-3:]))