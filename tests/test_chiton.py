import pytest

from helpers.grid import grid_of_values
from helpers.graph import all_nodes_with_children


@pytest.fixture
def mock_grid():
    return grid_of_values("./data/test_data_15.txt")


def test_all_nodes_with_children(mock_grid):
    assert len(all_nodes_with_children(mock_grid)) == 100

