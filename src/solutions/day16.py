from src.tools.loader import load_data
import networkx as nx
from itertools import product
from more_itertools import set_partitions
from tqdm import tqdm

TESTING = False


def parse_input(data):
    flow_rates = {}
    next_valves = {}

    for line in data:
        line1, line2 = line.split("; ")
        valve = line1.split(" ")[1]
        flow_rates[valve] = int(line1.split(" ")[-1].split("=")[-1])
        next_valves[valve] = tuple(line2.replace(",", "").split()[4:])

    return flow_rates, next_valves


def initialize_graph(flow_rates, next_valves):
    G = nx.DiGraph()

    for valve, flow_rate in flow_rates.items():
        G.add_node(valve, flow_rate=flow_rate)

    for current_valve, tunnels in next_valves.items():
        for next_valve in tunnels:
            G.add_edge(current_valve, next_valve)

    return G


def solve_part_1(G: nx.DiGraph, time):
    distances = {}
    predecessor_maps = {}

    for node in G.nodes:
        _predecessor_map, _distances = nx.algorithms.dijkstra_predecessor_and_distance(
            G, node
        )
        predecessor_maps[node] = _predecessor_map
        distances[node] = _distances

    def recurse(pos, closed_valves, time_left):
        if time_left <= 0:
            return 0
        best_value = 0
        for closed_valve in closed_valves:
            d = distances[pos][closed_valve]
            if time_left > d + 1:
                flow_rate = G.nodes[closed_valve]["flow_rate"]
                value = (time_left - d - 1) * flow_rate
                value += recurse(
                    closed_valve, closed_valves - {closed_valve}, time_left - d - 1
                )
                if value > best_value:
                    best_value = value

        return best_value

    return recurse("AA", {v for v in G.nodes if G.nodes[v]["flow_rate"] > 0}, time)


def solve_part_2(G: nx.DiGraph, time):
    distances = {}
    predecessor_maps = {}

    for node in G.nodes:
        _predecessor_map, _distances = nx.algorithms.dijkstra_predecessor_and_distance(
            G, node
        )
        predecessor_maps[node] = _predecessor_map
        distances[node] = _distances

    closed_valves = {v for v in G.nodes if G.nodes[v]["flow_rate"] > 0}
    distances = {
        (u, v): distances[u][v]
        for u, v in product(closed_valves | {"AA"}, repeat=2)
        if u != v
    }
    flow_rate = {v: G.nodes[v]["flow_rate"] for v in closed_valves}

    def recurse_part1(pos, closed_valves, time_left):
        if time_left <= 0:
            return 0

        best_value = 0
        for closed_valve in closed_valves:
            d = distances[(pos, closed_valve)]
            time_left_after_move = time_left - d - 1
            if time_left_after_move <= 0:
                continue
            value = time_left_after_move * flow_rate[closed_valve]
            value += recurse_part1(
                closed_valve, closed_valves - {closed_valve}, time_left_after_move
            )
            best_value = max(value, best_value)

        return best_value

    def recurse(closed_valves, time_left):
        best_value = 0
        for my_valves, elephant_valves in tqdm(
            set_partitions(closed_valves, 2),
            "go through all partitions",
            2 ** len(closed_valves) // 2,
        ):
            if len(my_valves) > len(elephant_valves):
                continue
            my_value = recurse_part1("AA", frozenset(my_valves), time_left)
            elephant_value = recurse_part1("AA", frozenset(elephant_valves), time_left)
            value = my_value + elephant_value
            best_value = max(best_value, value)

        return best_value

    return recurse(closed_valves, time)


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    flow_rates, next_valves = parse_input(data)
    G = initialize_graph(flow_rates, next_valves)

    # PART 1
    # test:   1651
    # answer: 2265
    print(solve_part_1(G, 30))

    # PART 2
    # test:   1707
    # answer: 2811
    print(solve_part_2(G, 26))
