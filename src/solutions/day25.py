from src.tools.loader import load_data

TESTING = False


def convert_to_base(base, number):
    result = ""
    while number > 0:
        result = str(number % base) + result
        number //= base
    return "0" if not result else result


def convert_snafu_to_dec(snafu):
    number = 0
    for i, item in enumerate(reversed(snafu)):
        value = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}[item]
        number += value * 5**i

    return number


def convert_dec_to_snafu(number):
    snafu = ""
    len_in_base_5 = len(convert_to_base(5, number))

    diff = int("2" * len_in_base_5, 5)
    if number > diff:
        diff += 2 * 5**len_in_base_5

    lifted = number + diff
    lifted_in_base_5 = convert_to_base(5, lifted)
    for char in lifted_in_base_5:
        snafu += {"0": "=", "1": "-", "2": "0", "3": "1", "4": "2"}[char]

    return snafu


if __name__ == "__main__":
    snafu_numbers = load_data(TESTING, "\n")
    decimal_sum = sum(map(convert_snafu_to_dec, snafu_numbers))

    # PART 1
    # test:                 2=-1=0 (4890)
    # answer: 2--1=0=-210-1=00=-=1 (33658310202841)

    print("Decimal sum:", decimal_sum)
    print("SNAFU sum:  ", convert_dec_to_snafu(decimal_sum))
