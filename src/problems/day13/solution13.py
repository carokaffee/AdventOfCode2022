from src.tools.loader import load_data

TESTING = True


def parse_input(data):
    result = []
    for pair in data:
        a, b = pair.split('\n')
        result.append(eval(a))
        result.append(eval(b))
    return result


def compare_integers(a,b):
    if a < b:
        return True
    elif a > b:
        return False
    else:
        return 'continue'


def compare_lists(a,b):
    length = min(len(a), len(b))
    if len(a) == 0 and len(b) == 0:
        return 'continue'
    elif len(b) == 0:
        return False
    elif len(a) == 0:
        return True
    for i in range(length):
        if compare(a[i], b[i]) == True:
            return True
        elif compare(a[i], b[i]) == False:
            return False
    if len(a) > len(b):
        return False
    elif len(a) < len(b):
        return True
    else:
        return 'continue'


def compare(a,b):
    if type(a) == int and type(b) == int:
        return compare_integers(a,b)
    elif type(a) == int and type(b) == list:
        return compare_lists([a], b)
    elif type(a) == list and type(b) == int:
        return compare_lists(a, [b])
    else:
        return compare_lists(a,b)



if __name__ == '__main__':
    data = load_data(TESTING, '\n\n')
    signal = parse_input(data)
    correct_indices = []

    for i in range(len(signal) // 2):
        if compare(signal[2 * i], signal[2 * i + 1]):
            correct_indices.append(i+1)
        
    print(sum(correct_indices))

    signal2 = parse_input(data)
    signal2.append([[2]])
    signal2.append([[6]])

    for _ in range(1000):
        for i, signal in enumerate(signal2[:-1]):
            if not compare(signal2[i], signal2[i+1]):
                signal2[i], signal2[i+1] = signal2[i+1], signal2[i]

    a = 0
    b = 0
    for i, signals in enumerate(signal2):
        if signals == [[2]]:
            a = i+1
        if signals == [[6]]:
            b = i+1
    
    print(a,b,a*b)