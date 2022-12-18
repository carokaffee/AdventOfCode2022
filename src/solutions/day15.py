from src.tools.loader import load_data
from tqdm import tqdm


TESTING = False


def parse_input(data):
    sensors_beacons = {}
    for line in data:
        words = line.split()
        sensor_x = int(words[2][2:-1])
        sensor_y = int(words[3][2:-1])
        beacon_x = int(words[-2][2:-1])
        beacon_y = int(words[-1][2:])
        sensors_beacons[(sensor_x, sensor_y)] = (beacon_x, beacon_y)

    return sensors_beacons


def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def is_within_distance(p1, p2, dist):
    dist_p = manhattan_dist(p1, p2)
    return dist_p <= dist


def get_dimensions():
    min_x = min(
        [x for x, _ in set(sensors_beacons.keys()).union(sensors_beacons.values())]
    )
    max_x = max(
        [x for x, _ in set(sensors_beacons.keys()).union(sensors_beacons.values())]
    )
    max_dist = max([y for y in dist_to_closest_beacon.values()])

    return min_x, max_x, max_dist


def possible_beacons_in_row(row):
    occupied = set(sensors_beacons.values())
    counter = 0

    for x in range(min_x - max_dist, max_x + 1 + max_dist):
        is_in_distance = False
        for sensor, dist in dist_to_closest_beacon.items():
            if is_within_distance(sensor, (x, row), dist) and (x, row) not in occupied:
                is_in_distance = True

        counter += is_in_distance

    return counter


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    sensors_beacons = parse_input(data)
    dist_to_closest_beacon = {
        s: manhattan_dist(s, b) for s, b in sensors_beacons.items()
    }

    min_x, max_x, max_dist = get_dimensions()

    print(possible_beacons_in_row(2000000))

    DIM = 4000000

    possible_points = set()
    for sensor, dist in tqdm(dist_to_closest_beacon.items()):
        sens_x, sens_y = sensor
        for x in range(dist + 2):
            y = dist + 1 - x
            possible_points.update(
                set(
                    (
                        (sens_x + x, sens_y + y),
                        (sens_x - x, sens_y + y),
                        (sens_x + x, sens_y - y),
                        (sens_x - x, sens_y - y),
                    )
                )
            )
    print(len(possible_points))

    real_possible_points = set()
    for x, y in tqdm(possible_points):
        if x >= 0 and x <= DIM and y >= 0 and y <= DIM:
            real_possible_points.add((x, y))

    print(len(real_possible_points))

    for x, y in tqdm(real_possible_points):
        is_in_distance = False
        for sensor, dist in dist_to_closest_beacon.items():
            possibility = is_within_distance(sensor, (x, y), dist)
            if possibility:
                is_in_distance = True

        if not is_in_distance:
            print(x, y)
