import functools
from unittest.mock import patch

import pytest

from day_14.polymerization import feed_input, count_elements_after_steps, subtract_least_common_element_from_most

partial_input = functools.partial(feed_input, "./data/test_data_14.txt")


@pytest.mark.parametrize(
    "steps, expected", [
        (1, {"N": 2, "B": 2, "C": 2, "H": 1})
    ]
)
@patch("day_14.polymerization.feed_input", return_value=partial_input())
def test_count_elements_after_steps(mock_input, steps, expected):
    assert count_elements_after_steps(steps) == expected


@patch("day_14.polymerization.feed_input", return_value=partial_input())
def test_count_elements(mock_input):
    elements = count_elements_after_steps(40)
    assert elements.get("H") == 3849876073
    assert elements.get("B") == 2192039569602


@pytest.mark.parametrize(
    ["steps", "expected"],
    [
        (10, 1588), (40, 2188189693529)
    ]
)
@patch("day_14.polymerization.feed_input", return_value=partial_input())
def test_subtract_least_common_element_from_most(mock_input, steps, expected):
    assert subtract_least_common_element_from_most(steps) == expected


def test_real_count():
    with patch("day_14.polymerization.feed_input", return_value=feed_input("../day_14/data.txt")):
        assert subtract_least_common_element_from_most(10) == 2408
