import unittest.mock

import pytest

from day_09.smoke_functions import *

test_grid = [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
             [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
             [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
             [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
             [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]


@unittest.mock.patch("day_09.smoke_functions.grid", return_value=test_grid)
class TestSmoke:
    @pytest.mark.parametrize(
        ["coord", "neighbours"],
        [
            ((0, 0), [1, 3]), ((9, 0), [1, 1]), ((0, 4), [8, 8]), ((9, 4), [7, 9]), ((4, 1), [7, 9, 9, 7])
        ]
    )
    def test_get_neighbours(self, mocked_feed, coord, neighbours):
        assert list(get_neighbours(coord)) == neighbours

    def test_find_minima(self, mocked_feed):
        assert find_minima() == {(1, 0), (9, 0), (2, 2), (6, 4)}

    @pytest.mark.parametrize(
        ["minimum", "basin_size"],
        (
                ((1, 0), 3), ((9, 0), 9), ((2, 2), 14), ((6, 4), 9)
        )
    )
    def test_find_basin_size(self, mocked_feed, minimum, basin_size):
        assert find_basin_size(iter((minimum,))) == basin_size

    def test_find_three_largest_and_get_product(self, mocked_feed):
        assert find_three_largest_and_get_product() == 1134

    def test_find_all_basin_sizes(self, mocked_feed):
        assert list(find_all_basin_sizes()) == [3, 9, 9, 14]
