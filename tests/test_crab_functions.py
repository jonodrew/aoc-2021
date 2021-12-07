from typing import Iterator

import pytest
from day_07.crab_functions import calculate_fuel, calculate_minimum_fuel_slowly


@pytest.fixture
def test_data():
    return iter([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])


def test_data_generator() -> Iterator[int]:
    return iter([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])


def test_calculate_fuel(test_data):
    assert calculate_fuel(test_data, 2) == 37


def test_slow_calculation():
    assert calculate_minimum_fuel_slowly(test_data_generator) == 37
