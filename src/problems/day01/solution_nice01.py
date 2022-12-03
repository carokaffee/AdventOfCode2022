from src.tools.loader import load_data

TESTING = True

if __name__ == '__main__':
    data = load_data(TESTING, '\n\n')
    data = [list(map(int,item.split('\n'))) for item in data]
    elves = list(map(sum, data))
    
    # solution 1
    print(max(elves))

    # solution 2
    print(sum(sorted(elves)[-3:]))