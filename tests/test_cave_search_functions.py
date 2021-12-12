from day_12.cave_search_functions import parse_line, generate_all_connections
from day_12.classes import Cave


def mock_input():
    lines = """start-A
start-b
A-c
A-b
b-d"
A-end
b-end"""
    for line in lines.split("\n"):
        yield line.strip()


def test_parse_line():
    assert parse_line("gv-start") == {Cave("gv", False): [Cave("start", False)], Cave("start", False): [Cave("gv", False)]}


def test_generate_all_connections():
    all_connections = generate_all_connections(mock_input())
    assert len(all_connections) == 6
