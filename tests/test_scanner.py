from day_19.scanner import *


def test_assert_overlapping():
    scanner_one = [(0, 2, 0), (4, 1, 0), (3, 3, 0)]
    scanner_two = [(-1, -1, 0), (-5, 0, 0), (-2, 1, 0)]
    assert assert_overlapping(all_relative_distances(scanner_one), scanner_two, 3, 0)