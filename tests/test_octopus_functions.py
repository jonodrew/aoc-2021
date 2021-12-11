from unittest.mock import patch

import pytest

from day_11.octopus_functions import Octopus, step_n_times


@pytest.fixture
def small_step_zero():
    little_grid = """11111
    19991
    19191
    19991
    11111"""
    return (Octopus(x, y, int(level)) for y, line in enumerate(little_grid.split("\n")) for x, level in
            enumerate(line.strip()))


@patch("day_11.octopus_functions.grid_max_index", return_value=4)
class TestSmallGrid:
    @pytest.mark.parametrize(
        ["new_grid", "steps"],
        [
            ("""34543
40004
50005
40004
34543""", 1), ("""45654
51115
61116
51115
45654""", 2)
        ]
    )
    def test_step(self,  mock_height, new_grid, steps, small_step_zero):
        assert [octo.level for octo in step_n_times(steps, small_step_zero)] == [int(level) for y, line in
                                                                  enumerate(new_grid.split("\n")) for x, level in
                                                                  enumerate(line.strip())]
