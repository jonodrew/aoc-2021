from unittest.mock import patch

import pytest

from day_14.polymerization import process_polymer, feed_input


@pytest.mark.parametrize(
    ("steps", "expected"),
    [
        (1, "NCNBCHB"), (2, "NBCCNBBBCBHCB")
    ]
)
def test_process_polymer(steps, expected):
    with patch("day_14.polymerization.feed_input", return_value=feed_input("./data/test_data_14.txt")):
        assert process_polymer("NNCB", steps) == expected
