from src.tools.loader import load_data


TESTING = False


def parse_input(data):
    closest_beacon = {}
    for line in data:
        words = line.split()
        sensor_x = int(words[2][2:-1])
        sensor_y = int(words[3][2:-1])
        beacon_x = int(words[-2][2:-1])
        beacon_y = int(words[-1][2:])
        closest_beacon[(sensor_x, sensor_y)] = (beacon_x, beacon_y)

    return closest_beacon


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def is_within_distance(p1, p2, dist):
    dist_p = manhattan_distance(p1, p2)
    return dist_p <= dist


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    closest_beacon = parse_input(data)
    dist_to_closest_beacon = {
        sensor: manhattan_distance(sensor, beacon)
        for sensor, beacon in closest_beacon.items()
    }
    # print(closest_beacon)
    # print(dist_to_closest_beacon)

    min_x = min(
        [x for x, y in set(closest_beacon.keys()).union(closest_beacon.values())]
    )
    min_y = min(
        [y for x, y in set(closest_beacon.keys()).union(closest_beacon.values())]
    )
    max_x = max(
        [x for x, y in set(closest_beacon.keys()).union(closest_beacon.values())]
    )
    max_y = max(
        [y for x, y in set(closest_beacon.keys()).union(closest_beacon.values())]
    )
    max_dist = max([y for y in dist_to_closest_beacon.values()])
    print(min_x, min_y, max_x, max_y)

    Y_ROW = 2000000
    occupied = set(closest_beacon.values())

    counter = 0
    for x in range(min_x - max_dist, max_x + 1 + max_dist):
        is_in_distance = False
        for sensor, dist in dist_to_closest_beacon.items():
            possibility = is_within_distance(sensor, (x, Y_ROW), dist)
            if possibility:
                if (x, Y_ROW) not in occupied:
                    is_in_distance = True
            # print(dist, manhattan_distance((x, Y_ROW), sensor))

        if is_in_distance:
            # print(x)
            counter += 1
            # print()

    print(counter)
