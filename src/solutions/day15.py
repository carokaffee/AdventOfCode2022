from src.tools.loader import load_data
from tqdm import tqdm
from itertools import combinations


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
    dist_p1_p2 = manhattan_dist(p1, p2)
    return dist_p1_p2 <= dist


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
    min_x, max_x, max_dist = get_dimensions()

    for x in tqdm(range(min_x - max_dist, max_x + 1 + max_dist), "go through row"):
        is_in_distance = False
        for sensor, dist in dist_to_closest_beacon.items():
            if is_within_distance(sensor, (x, row), dist) and (x, row) not in occupied:
                is_in_distance = True

        counter += is_in_distance

    return counter


def tuning_frequency(DIM):
    possible_points = {sensor: set() for sensor in sensors_beacons.keys()}
    for sensor, dist in tqdm(dist_to_closest_beacon.items(), "store feasible edges"):
        sens_x, sens_y = sensor
        new_possible_points = set()
        for x in range(dist + 2):
            y = dist + 1 - x
            new_possible_points.update(
                set(
                    (
                        (sens_x + x, sens_y + y),
                        (sens_x - x, sens_y + y),
                        (sens_x + x, sens_y - y),
                        (sens_x - x, sens_y - y),
                    )
                )
            )
        for x, y in new_possible_points:
            if x >= 0 and x <= DIM and y >= 0 and y <= DIM:
                possible_points[sensor].add((x, y))

    intersection_points = set()
    for sensor1, sensor2 in tqdm(
        combinations(sensors_beacons.keys(), 2),
        "find intersections",
        len(sensors_beacons.keys()) * (len(sensors_beacons.keys()) - 1) // 2,
    ):
        intersecting = possible_points[sensor1].intersection(possible_points[sensor2])
        if len(intersecting) <= 2:
            intersection_points.update(intersecting)

    for x, y in tqdm(intersection_points, "check all possible points"):
        is_in_distance = False
        for sensor, dist in dist_to_closest_beacon.items():
            is_in_distance = is_in_distance or is_within_distance(sensor, (x, y), dist)

        if not is_in_distance:
            only_intersection = (x, y)
            break

    return only_intersection[0] * 4000000 + only_intersection[1]


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    sensors_beacons = parse_input(data)
    dist_to_closest_beacon = {
        s: manhattan_dist(s, b) for s, b in sensors_beacons.items()
    }

    ROW = 10 if TESTING else 2000000
    DIM = 20 if TESTING else 4000000

    # PART 1
    # test:        26
    # answer: 6078701
    print("Solution for part 1:", possible_beacons_in_row(ROW))

    # PART 2
    # test:         56000011
    # answer: 12567351400528
    print("Solution for part 2:", tuning_frequency(DIM))
