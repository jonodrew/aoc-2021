import pytest

from day_06.fish_functions import *


@pytest.fixture
def day_zero():
    return iter((3, 4, 3, 1, 2))


@pytest.mark.parametrize(
    ["day", "expected"],
    [
        (0, 5), (18, 26), (80, 5934), (256, 26984457539)
    ]
)
def test_population_on_day(day_zero, day, expected):
    assert population_on_day(day, day_zero) == expected


@pytest.mark.parametrize(
    ["initial", "expected"],
    [
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8, 0]),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9], [2, 3, 4, 5, 6, 7, 9, 9, 1])
    ]
)
def test_move_along(initial, expected):
    assert list(move_along(iter(initial))) == expected
