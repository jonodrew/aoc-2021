from unittest.mock import patch

from day_12.cave_search_functions import parse_line, generate_all_connections, explore_every_path, \
    count_all_paths_when_visiting_one_small_twice
from day_12.classes import Cave


def mock_input():
    lines = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    for line in lines.split("\n"):
        yield line.strip()


def test_parse_line():
    assert parse_line("gv-start") == {Cave("gv", False): [Cave("start", False)],
                                      Cave("start", False): [Cave("gv", False)]}


def test_generate_all_connections():
    all_connections = generate_all_connections(mock_input())
    assert len(all_connections) == 6


def test_explore_every_path():
    mock_cave_map = generate_all_connections(mock_input())
    expected = """start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end"""
    expected_set = {line for line in expected.split("\n")}
    with patch("day_12.cave_search_functions.feed_input", return_value=mock_input()):
        assert {','.join((cave.name for cave in path)) for path in
                explore_every_path()} == expected_set


def test_count_all_paths_when_visiting_one_small_twice():
    with patch("day_12.cave_search_functions.feed_input", return_value=mock_input()):
        assert count_all_paths_when_visiting_one_small_twice() == 36
