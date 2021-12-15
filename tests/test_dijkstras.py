import pytest

from helpers.dijkstras import dijkstras_algorithm
from helpers.graph import Node, initial_grid_of_nodes
from helpers.grid import grid_of_values


@pytest.fixture
def node_list():
    return initial_grid_of_nodes(grid_of_values("./data/test_data_15.txt"))


def test_dijkstras_algorithm(node_list):
    assert sum(map(lambda node: node.risk, dijkstras_algorithm(node_list.get((0, 0)), dict(), grid_of_values("./data/test_data_15.txt"), frozenset({}), frozenset({})))) == 40
