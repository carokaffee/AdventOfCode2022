from src.tools.loader import load_data

TESTING = True

if __name__ == '__main__':
    data = load_data(TESTING, '\n')
    games = [(a,b) for a,b in [el.split() for el in data]]
    score_1 = 0
    score_2 = 0
    
    for a,b in games:
        if b == 'X':
            score_1 += 1
        elif b == 'Y':
            score_1 += 2
        elif b == 'Z':
            score_1 += 3
        if (a == 'A' and b == 'X') or (a == 'B' and b == 'Y') or (a == 'C' and b == 'Z'):
            score_1 += 3
        elif (a == 'A' and b == 'Y') or (a == 'B' and b == 'Z') or (a == 'C' and b == 'X'):
            score_1 += 6
        elif (a == 'A' and b == 'Z') or (a == 'B' and b == 'X') or (a == 'C' and b == 'Y'):
            score_1 += 0

    for a,b in games:
        if b == 'X':
            score_2 += 0
        elif b == 'Y':
            score_2 += 3
        elif b == 'Z':
            score_2 += 6
        if (a == 'A' and b == 'Y') or (a == 'B' and b == 'X') or (a == 'C' and b == 'Z'):
            score_2 += 1
        elif (a == 'A' and b == 'Z') or (a == 'B' and b == 'Y') or (a == 'C' and b == 'X'):
            score_2 += 2
        elif (a == 'A' and b == 'X') or (a == 'B' and b == 'Z') or (a == 'C' and b == 'Y'):
            score_2 += 3

    print(score_1)
    print(score_2)