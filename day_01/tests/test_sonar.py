import pytest

from day_01.source import cast_data_to_int, solve_part_one, generate_three_measurements, solve_part_two
from helpers import current_path, stream_data


@pytest.fixture
def data_stream():
    return cast_data_to_int(stream_data(current_path(__file__)))


def test_sonar_data(data_stream):
    assert list(data_stream) == [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_sonar_solve(data_stream):
    assert solve_part_one(data_stream) == 7


def test_chunking(data_stream):
    assert list(generate_three_measurements(data_stream)) == [607, 618, 618, 617, 647, 716, 769, 792]


def test_part_two(data_stream):
    assert solve_part_two(data_stream) == 5
