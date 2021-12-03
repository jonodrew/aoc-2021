import functools

import pytest

from day_03.functions import (
    commonest_bit,
    generate_new_numbers,
    gamma_rate,
    epsilon_rate,
    solve_part_one,
    recursive_find_rating,
    least_common_bit,
    solve_part_two,
)
from helpers import stream_data, current_path


@pytest.fixture
def test_data_stream():
    return stream_data(current_path(__file__))


def test_commonest_bit_at_position(test_data_stream):
    bit_to_find = commonest_bit(generate_new_numbers(test_data_stream).__next__())
    assert bit_to_find == "1"


def test_gamma_rate(test_data_stream):
    assert gamma_rate(test_data_stream) == "10110"


def test_epsilon_rate(test_data_stream):
    assert epsilon_rate(gamma_rate(test_data_stream)) == "01001"


def test_solve_part_one(test_data_stream):
    assert solve_part_one(test_data_stream) == 198


@pytest.mark.parametrize(
    ["bit_function", "expected"],
    [
        (functools.partial(commonest_bit, bit_if_equal="1"), "10111"),
        (least_common_bit, "01010"),
    ],
)
def test_recursive_find_rating(bit_function, expected, test_data_stream):
    assert recursive_find_rating(test_data_stream, bit_function) == expected


def test_solve_part_two(test_data_stream):
    assert solve_part_two(test_data_stream) == 230
