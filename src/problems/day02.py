from src.tools.loader import load_data

TESTING = False


def parse_input(game):
    you, me = game.split()
    mapping = ({"A": 0, "B": 1, "C": 2}[you], {"X": 0, "Y": 1, "Z": 2}[me])
    return mapping


def score_game_1(you, me):
    game_score = ((me - you + 1) % 3) * 3
    item_score = me + 1
    return game_score + item_score


def score_game_2(you, me):
    game_score = me * 3
    item_score = (you + me - 1) % 3 + 1
    return game_score + item_score


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    games = list(map(parse_input, data))
    score_1 = 0
    score_2 = 0

    for game in games:
        score_1 += score_game_1(*game)
        score_2 += score_game_2(*game)

    # PART 1
    # test:      15
    # answer: 11841
    print(score_1)

    # PART 2
    # test:      12
    # answer: 13022
    print(score_2)
