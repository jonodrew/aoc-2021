from day_08.display_functions import *
from unittest.mock import patch


def test_parse_input():
    with patch("day_08.display_functions.feed_input", return_value=iter(
            ("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",))):
        assert next(parse_input()) == (
            ['be', 'cfbegad', 'cbdgef', 'fgaecd', 'cgeb', 'fdcge', 'agebfd', 'fecdb', 'fabcd', 'edb'],
            ['fdgacbe', 'cefdb', 'cefbgd', 'gcbe'])


def test_count_unique_numbers():
    with open("/Users/jonathankerr/projects/aoc-2021/tests/test_data/day_08_data.txt", "r") as test_file:
        with patch("day_08.display_functions.feed_input", return_value=test_file.readlines()):
            assert count_ones_fours_sevens_eights() == 26


def test_recursively_calculate_mapping():
    test_line = iter(['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'])
    expected_mapping = {
        8: set("acedgfb"),
        5: set("cdfbe"),
        2: set("gcdfa"),
        3: set("fbcad"),
        7: set("dab"),
        9: set("cefabd"),
        6: set("cdfgeb"),
        4: set("eafb"),
        0: set("cagedb"),
        1: set("ab")
    }
    assert recursively_calculate_mapping(test_line, {}) == expected_mapping


def test_decode_display():
    final_mapping = {
        8: set("acedgfb"),
        5: set("cdfbe"),
        2: set("gcdfa"),
        3: set("fbcad"),
        7: set("dab"),
        9: set("cefabd"),
        6: set("cdfgeb"),
        4: set("eafb"),
        0: set("cagedb"),
        1: set("ab")
    }
    assert decode_display(final_mapping, ["cdfeb", "fcadb", "cdfeb", "cdbaf"]) == "5353"


def test_solve_part_two():
    with open("/Users/jonathankerr/projects/aoc-2021/tests/test_data/day_08_data.txt", "r") as test_file:
        with patch("day_08.display_functions.feed_input", return_value=test_file.readlines()):
            assert sum(map(int, decode_all_displays())) == 61229
