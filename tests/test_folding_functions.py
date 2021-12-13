import functools
from unittest.mock import patch

import helpers
from day_13.folding_functions import fold_paper, feed_input, grid_of_dots


def mock_input():
    return functools.partial(feed_input, "./data/test_data_13.txt")


@patch("day_13.folding_functions.feed_input", return_value=mock_input)
def test_fold_paper(mock_feed):
    initial_grid = functools.partial(grid_of_dots, mock_input())
    assert helpers.iterator_length(fold_paper("y=7", initial_grid())) == 17
    assert helpers.iterator_length(fold_paper("x=5", fold_paper("y=7", initial_grid()))) == 16
