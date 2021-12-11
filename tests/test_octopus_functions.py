from unittest.mock import patch

import pytest

from day_11.octopus_functions import step, Octopus


@pytest.fixture
def small_step_zero():
    little_grid = """11111
    19991
    19191
    19991
    11111"""
    return (Octopus(x, y, int(level)) for y, line in enumerate(little_grid.split("\n")) for x, level in enumerate(line.strip()))


@patch("day_11.octopus_functions.grid_height", return_value=5)
class TestSmallGrid:
    def test_step(self, mock_height, small_step_zero):
        new_grid = """34543
40004
50005
40004
34543"""
        assert [octo.level for octo in step(small_step_zero)] == [int(level) for y, line in enumerate(new_grid.split("\n")) for x, level in enumerate(line.strip())]
