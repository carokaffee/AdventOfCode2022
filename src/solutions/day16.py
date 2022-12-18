from src.tools.loader import load_data
import networkx as nx

TESTING = True


def parse_input(data):
    flow_rates = {}
    next_tunnels = {}
    for line in data:
        flow, tunnels = line.split("; ")
        valve = flow.split(" ")[1]
        flow_rate = int(flow.split(" ")[-1].split("=")[-1])
        next_tunnel = tuple(tunnels.replace(",", "").split()[4:])
        flow_rates[valve] = flow_rate
        next_tunnels[valve] = next_tunnel
    return flow_rates, next_tunnels


def solve(G: nx.DiGraph, time=30):
    distances = {}
    predecessor_maps = {}
    for node in G.nodes:
        _predecessor_map, _distances = nx.algorithms.dijkstra_predecessor_and_distance(
            G, node
        )
        predecessor_maps[node] = _predecessor_map
        distances[node] = _distances

    position = "AA"

    def recurse(pos: str, closed_valves: set[str], time_left: int):
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

    return recurse(position, {v for v in G.nodes if G.nodes[v]["flow_rate"] > 0}, time)


def solve2(G: nx.DiGraph, time=26):
    distances = {}
    predecessor_maps = {}
    for node in G.nodes:
        _predecessor_map, _distances = nx.algorithms.dijkstra_predecessor_and_distance(
            G, node
        )
        predecessor_maps[node] = _predecessor_map
        distances[node] = _distances

    position1 = "AA"
    position2 = "AA"

    def recurse(
        pos1: str,
        pos2: str,
        left1: int,
        left2: int,
        closed_valves: set[str],
        time_left: int,
    ):
        if time_left <= 0:
            return 0
        best_value = 0

        if len(closed_valves) == 1:
            for closed in closed_valves:
                d1 = distances[pos1][closed]
                d2 = distances[pos2][closed]
                if time_left > min(d1 + 1, d2 + 1):
                    if d1 <= d2:
                        flow_rate1 = G.nodes[closed]["flow_rate"]
                        value = (time_left - d1 - 1) * flow_rate1
                        value += recurse(
                            closed,
                            closed,
                            left1,
                            left2,
                            closed_valves - {closed},
                            time_left - d1 - 1,
                        )
                        if value > best_value:
                            best_value = value

        for closed1 in closed_valves:
            for closed2 in closed_valves - {closed1}:
                if left1 == 0 and left2 == 0:
                    d1 = distances[pos1][closed1]
                    d2 = distances[pos2][closed2]

                    if time_left > min(d1 + 1, d2 + 1):
                        flow_rate1 = G.nodes[closed1]["flow_rate"]
                        flow_rate2 = G.nodes[closed2]["flow_rate"]
                        value = (time_left - d1 - 1) * (flow_rate1 + flow_rate2)
                        value += recurse(
                            closed1,
                            closed2,
                            left1,
                            left2,
                            closed_valves - {closed2, closed1},
                            time_left - d1 - 1,
                        )
                        if value > best_value:
                            best_value = value

                elif left1 == 0 and left2 > 0:
                    d1 = distances[pos1][closed1]

                    if time_left > min(d1 + 1, left2 + 1):
                        if d1 > left2:
                            flow_rate2 = G.nodes[pos2]["flow_rate"]
                            value = (time_left - left2 - 1) * flow_rate2
                            value += recurse(
                                closed1,
                                closed2,
                                d1 - left2 - 1,
                                0,
                                closed_valves - {pos2},
                                time_left - left2 - 1,
                            )
                            if value > best_value:
                                best_value = value
                        elif d1 < left2:
                            flow_rate1 = G.nodes[closed1]["flow_rate"]
                            value = (time_left - d1 - 1) * flow_rate1
                            value += recurse(
                                closed1,
                                pos2,
                                left1,
                                left2 - d1 - 1,
                                closed_valves - {closed1},
                                time_left - d1 - 1,
                            )
                            if value > best_value:
                                best_value = value

                        else:
                            flow_rate1 = G.nodes[closed1]["flow_rate"]
                            flow_rate2 = G.nodes[pos2]["flow_rate"]
                            value = (time_left - d1 - 1) * (flow_rate1 + flow_rate2)
                            value += recurse(
                                closed1,
                                pos2,
                                0,
                                0,
                                closed_valves - {closed1, pos2},
                                time_left - d1 - 1,
                            )
                            if value > best_value:
                                best_value = value

                elif left1 > 0 and left2 == 0:
                    ...

        return best_value

    return recurse(
        position1,
        position2,
        {v for v in G.nodes if G.nodes[v]["flow_rate"] > 0},
        time,
    )


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    flow_rates, next_tunnels = parse_input(data)
    valve_opened_initial = {key: False for key in flow_rates.keys()}
    for valve in flow_rates.keys():
        if flow_rates[valve] == 0:
            valve_opened_initial[valve] = True

    G = nx.DiGraph()

    for valve, flow_rate in flow_rates.items():
        G.add_node(valve, flow_rate=flow_rate)

    for current_valve, tunnels in next_tunnels.items():
        for next_valve in tunnels:
            G.add_edge(current_valve, next_valve)

    print(solve(G, 30))
    print(solve2(G, 26))
