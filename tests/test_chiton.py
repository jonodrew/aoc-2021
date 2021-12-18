from unittest.mock import patch

import pytest

from day_15.chiton import dijkstras_algorithm, gen_reference_grid


@pytest.fixture
def mock_grid():
    return gen_reference_grid("./data/test_data_15.txt")


def test_dijkstras(mock_grid):
    with patch("day_15.chiton.gen_reference_grid", return_value=mock_grid):
        assert dijkstras_algorithm(mock_grid).cost == 40


def test_big_dijkstras(mock_grid):
    with patch("day_15.chiton.gen_reference_grid", return_value=mock_grid):
        last_node = dijkstras_algorithm(mock_grid, 5)
        assert last_node.cost == 315