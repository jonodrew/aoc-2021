from helpers.dijkstras import dijkstras_algorithm
from helpers.graph import Node
from helpers.grid import grid_of_values


def solve_part_one():
    risk_grid = grid_of_values("data.txt")
    start_node = Node(0, 0, risk_grid.get((0, 0)))
    return dijkstras_algorithm(
        start_node,
        {start_node: 0},
        risk_grid,
        lambda: (99, 99),
        dict()
    )

solve_part_one()