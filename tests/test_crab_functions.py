from typing import Iterator

import pytest
from day_07.crab_functions import calculate_total_fuel_for_point, calculate_minimum_fuel, minimum_of_curve, absolute_distance


@pytest.fixture
def test_data():
    return test_data_generator()


def test_data_generator() -> Iterator[int]:
    return iter(sorted([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]))


def test_calculate_fuel(test_data):
    assert calculate_total_fuel_for_point(absolute_distance, 2, test_data) == 37


def test_slow_calculation():
    assert calculate_minimum_fuel(test_data_generator) == 37


def test_slow_calculation_exponential():
    assert calculate_minimum_fuel(test_data_generator, True) == 168


def test_minimum_of_curve():
    assert minimum_of_curve(3, iter((2, 1, 2, 3))) == 1
