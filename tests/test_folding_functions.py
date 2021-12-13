import functools
from unittest.mock import patch

import helpers
from day_13.folding_functions import follow_instruction, feed_input, grid_of_dots, pretty_print, follow_all_instructions, instructions


def mock_input():
    return functools.partial(feed_input, "./data/test_data_13.txt")


@patch("day_13.folding_functions.feed_input", return_value=mock_input)
def test_fold_paper(mock_feed):
    initial_grid = functools.partial(grid_of_dots, mock_input())
    assert helpers.iterator_length(follow_instruction("y=7", initial_grid())) == 17
    assert helpers.iterator_length(follow_instruction("x=5", follow_instruction("y=7", initial_grid()))) == 16


def test_pretty_print():
    expected = """#####
#...#
#...#
#...#
#####"""
    assert '\n'.join(pretty_print(follow_all_instructions(grid_of_dots(mock_input()), instructions(mock_input())))) == expected
