from src.tools.loader import load_data
from tqdm import tqdm
from pulp import (
    LpProblem,
    LpMaximize,
    LpVariable,
    LpAffineExpression,
    lpSum,
    value,
    PULP_CBC_CMD,
)

TESTING = False


def parse_input(data):
    blueprints = []

    for line in data:
        p1, p2 = line.split(": ")
        blueprint = int(p1.split()[1]) - 1
        blueprints.append({})
        robots = p2.strip(".").split(". ")
        for robot in robots:
            _, type, _, _, *costs = robot.split(" ")
            blueprints[blueprint][type] = {material: 0 for material in MATERIALS}
            material_costs = " ".join(costs).split(" and ")
            for material in material_costs:
                cost, mat = material.split(" ")
                blueprints[blueprint][type][mat] = int(cost)

    return blueprints


def solve_lp(blueprint, timesteps):
    # initialise LP program
    robots_lp = LpProblem("Robots_LP", LpMaximize)

    # variables: robots of type 'material' bought at timestep 'i'
    variables = []
    for i in range(timesteps + 1):
        for mat in MATERIALS:
            variables.append(f"{i:02}_{mat}")
    lp_variables = LpVariable.dicts("Variables", variables, cat="Binary")

    # objective function: maximise geodes
    robots_lp += LpAffineExpression(
        [
            (lp_variables[x], timesteps - int(x.split("_")[0]))
            for x in lp_variables.keys()
            if "geode" in x
        ]
    )

    # start with one ore robot
    robots_lp += lp_variables["00_ore"] == 1

    # constraint: only one robot per timestep
    for i in range(timesteps + 1):
        robots_lp += (
            lpSum([lp_variables[x] for x in lp_variables if f"{i:02}_" in x]) <= 1
        ), f"one_robot_per_timestep_{i:02}"

    # constaint: buy only if you have enough material
    for material in MATERIALS:
        for timestep in range(timesteps + 1):
            relevant_vars = [
                x for x in lp_variables if int(x.split("_")[0]) <= timestep
            ]
            total_material = LpAffineExpression(
                (lp_variables[x], timestep - int(x.split("_")[0]) - 1)
                for x in relevant_vars
                if ((material in x) and (f"{timestep:02}" not in x))
            )
            spent_material = LpAffineExpression(
                (
                    lp_variables[x],
                    blueprint[x.split("_")[1]][material],
                )
                for x in relevant_vars
                if "00" not in x
            )

            robots_lp += (
                total_material - spent_material >= 0,
                f"enough_material_of_kind_{material}_at_time_{timestep:02}",
            )

    # solve LP
    robots_lp.solve(PULP_CBC_CMD(msg=0))

    return int(value(robots_lp.objective))


def sum_of_quality_levels(blueprints, timesteps):
    sum_of_levels = 0
    for i, blueprint in tqdm(
        enumerate(blueprints), "solve LPs for part 1", len(blueprints)
    ):
        sum_of_levels += (i + 1) * solve_lp(blueprint, timesteps)

    return sum_of_levels


def product_of_quality_levels(blueprints, timesteps):
    prod_of_levels = 1
    for blueprint in tqdm(blueprints[:3], "solve LPs for part 2", 3):
        prod_of_levels *= solve_lp(blueprint, timesteps)

    return prod_of_levels


if __name__ == "__main__":
    data = load_data(TESTING, "\n")
    MATERIALS = {"ore", "clay", "obsidian", "geode"}
    blueprints = parse_input(data)

    # PART 1
    # test:    33
    # answer: 851
    print(sum_of_quality_levels(blueprints, 24))

    # PART 2
    # test:    3472
    # answer: 12160
    print(product_of_quality_levels(blueprints, 32))
