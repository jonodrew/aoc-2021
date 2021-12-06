import pytest

from day_06.fish_functions import *


@pytest.fixture
def day_zero():
    return fish_generator((LanternFish(timer) for timer in (3, 4, 3, 1, 2)))


@pytest.mark.parametrize(
    ["day", "expected"],
    [
        (0, 5), (18, 26), (80, 5934)
    ]
)
def test_population_on_day(day_zero, day, expected):
    assert population_on_day(day, day_zero) == expected
