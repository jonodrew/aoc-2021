import pytest

from day_09.smoke_functions import *


@pytest.fixture
def test_grid():
    return [[2, 1, 9, 9, 9, 4, 3, 2, 1, 0],
            [3, 9, 8, 7, 8, 9, 4, 9, 2, 1],
            [9, 8, 5, 6, 7, 8, 9, 8, 9, 2],
            [8, 7, 6, 7, 8, 9, 6, 7, 8, 9],
            [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]


@pytest.mark.parametrize(
    ["coord", "neighbours"],
    [
        ((0, 0), [1, 3]), ((9, 0), [1, 1]), ((0, 4), [8, 8]), ((9, 4), [7, 9]), ((4, 1), [7, 9, 9, 7])
    ]
)
def test_get_neighbours(test_grid, coord, neighbours):
    assert get_neighbours(coord, test_grid) == neighbours


def test_find_minima(test_grid):
    assert find_minima(test_grid) == {(1, 0), (9, 0), (2, 2), (6, 4)}
