import pytest

from day_02.source import solve_part_one, solve_part_two, calculate_position_and_aim
from helpers import current_path, stream_data


@pytest.fixture
def test_data_stream():
    return stream_data(current_path(__file__))


def test_solve_part_one(test_data_stream):
    assert solve_part_one(test_data_stream) == 150


def test_solve_part_two(test_data_stream):
    assert solve_part_two(test_data_stream) == 900


def test_calculate_position_and_aim():
    current = 0, 0, 0
    instruction = 5, 0
    assert calculate_position_and_aim(current, instruction) == (5, 0, 0)
