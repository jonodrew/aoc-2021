from day_04.bingo_functions import (
    parse_data,
    Value,
    solve_bingo_part_one,
    solve_bingo_part_two,
    check_lines_in_one_direction,
)
import pytest


@pytest.fixture
def line():
    return (Value(0, 0, 0, i) for i in range(5))


@pytest.fixture
def column(line):
    return (Value(v.number, v.col, v.board, v.number, True) for v in line)


@pytest.fixture
def row(line):
    return (Value(v.row, v.number, v.board, v.number, True) for v in line)


@pytest.fixture
def incomplete_line(column):
    return (
        Value(v.row, v.col, v.board, v.number, False) if v.number == 2 else v
        for v in column
    )


@pytest.fixture
def test_data():
    return parse_data("./tests_day_04")


def test_parse_data(test_data):
    data = list(test_data)
    assert data[0] == [
        7,
        4,
        9,
        5,
        11,
        17,
        23,
        2,
        0,
        14,
        21,
        24,
        10,
        16,
        13,
        6,
        15,
        25,
        12,
        22,
        18,
        20,
        8,
        19,
        3,
        26,
        1,
    ]
    assert data[1] == [22, 13, 17, 11, 0]


@pytest.mark.parametrize(
    "line_values, direction, expected",
    [("row", "row", True), ("column", "col", True), ("incomplete_line", "col", False)],
)
def test_check_all_lines(line_values, direction, expected, request):
    assert (
        check_lines_in_one_direction(request.getfixturevalue(line_values), direction)
        is expected
    )


def test_solve_part_one(test_data):
    assert solve_bingo_part_one(test_data) == 4512


def test_solve_part_two(test_data):
    assert solve_bingo_part_two(test_data) == 1924
