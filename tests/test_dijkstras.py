import pytest

from helpers.dijkstras import dijkstras_algorithm
from helpers.graph import Node, initial_grid_of_nodes
from helpers.grid import grid_of_values


@pytest.fixture
def node_list():
    return initial_grid_of_nodes(grid_of_values("./data/test_data_15.txt"))


def test_dijkstras_algorithm(node_list):
    start_node = node_list.get((0, 0))
    grid_size = lambda: (9, 9)
    best_path, closest_parents, distances = dijkstras_algorithm(start_node, {start_node: 0}, grid_of_values("./data/test_data_15.txt"), grid_size, dict(), frozenset({}), frozenset({}))
    assert distances.get(Node(9, 9, 1)) == 40
