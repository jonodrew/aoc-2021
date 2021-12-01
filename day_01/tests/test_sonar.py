import pytest

from day_01.source import (
    cast_data_to_int,
    generate_three_measurements,
    compare_measurements,
    multiply_and_zip_with_offset,
)
from helpers import current_path, stream_data


@pytest.fixture
def test_data_stream():
    return cast_data_to_int(stream_data(current_path(__file__)))


def test_sonar_data(test_data_stream):
    assert list(test_data_stream) == [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_sonar_solve(test_data_stream):
    assert compare_measurements(test_data_stream) == 7


def test_chunking(test_data_stream):
    assert list(generate_three_measurements(test_data_stream)) == [
        607,
        618,
        618,
        617,
        647,
        716,
        769,
        792,
    ]


def test_part_two(test_data_stream):
    assert compare_measurements(generate_three_measurements(test_data_stream)) == 5


def test_multiply_and_zip_with_offset(test_data_stream):
    assert list(multiply_and_zip_with_offset(test_data_stream, 2)) == [
        (199, 200),
        (200, 208),
        (208, 210),
        (210, 200),
        (200, 207),
        (207, 240),
        (240, 269),
        (269, 260),
        (260, 263),
    ]
