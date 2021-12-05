import functools

import pytest

from day_05.vent_functions import *


def test_parse_datum():
    assert parse_datum("0,9 -> 5,9") == LineSegment(Point(0, 9), Point(5, 9))


@pytest.mark.parametrize(
    ["string_to_parse", "partial_coord", "partial_value", "range_from", "range_to"],
    [
        ("0,9 -> 5,9", "y", 9, 0, 6), ("2,2 -> 2,1", "x", 2, 1, 3)
    ]
)
def test_generate_all_integer_points(string_to_parse, partial_coord, partial_value, range_from, range_to):
    line = parse_datum(string_to_parse)
    kwargs = {partial_coord: partial_value}
    half_point = functools.partial(Point, **kwargs)
    remaining_coord = "x" if partial_coord == "y" else "y"
    assert set(generate_all_integer_points(line)) == set(map(lambda x: half_point(**{remaining_coord: x}), (i for i in range(range_from, range_to))))
