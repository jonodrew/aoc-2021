import unittest.mock

import pytest

from day_09.smoke_functions import get_neighbours, find_minima, find_basin_size, find_three_largest_and_get_product, \
    find_all_basin_sizes

test_grid = lambda: ((2, 1, 9, 9, 9, 4, 3, 2, 1, 0),
             (3, 9, 8, 7, 8, 9, 4, 9, 2, 1),
             (9, 8, 5, 6, 7, 8, 9, 8, 9, 2),
             (8, 7, 6, 7, 8, 9, 6, 7, 8, 9),
             (9, 8, 9, 9, 9, 6, 5, 6, 7, 8))


@pytest.mark.parametrize(
        ["coord", "neighbours"],
        [
            ((0, 0), [1, 3]), ((9, 0), [1, 1]), ((0, 4), [8, 8]), ((9, 4), [7, 9]), ((4, 1), [7, 9, 9, 7])
        ]
    )
def test_get_neighbours(coord, neighbours):
    assert list(get_neighbours(coord, test_grid)) == neighbours


def test_find_minima():
    assert find_minima(test_grid) == frozenset({(1, 0), (9, 0), (2, 2), (6, 4)})


@pytest.mark.parametrize(
        ["minimum", "basin_size"],
        (
                ((1, 0), 3), ((9, 0), 9), ((2, 2), 14), ((6, 4), 9)
        )
    )
def test_find_basin_size(minimum, basin_size):
    assert find_basin_size(test_grid, iter((minimum,))) == basin_size


def test_find_all_basin_sizes():
    assert list(find_all_basin_sizes(test_grid)) == [3, 9, 9, 14]


def test_find_three_largest_and_get_product():
    assert find_three_largest_and_get_product(test_grid) == 1134




