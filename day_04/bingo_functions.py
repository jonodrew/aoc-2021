import itertools
from dataclasses import dataclass
from typing import Generator, List, Union, Tuple, Iterator

from helpers import stream_data, partition, iterator_length


@dataclass
class Value:
    row: int
    col: int
    board: int
    number: int


def parse_data(file_path):
    for i, line in enumerate(stream_data(file_path)):
        if i == 0:
            yield [int(number) for number in line.split(",")]
        else:
            if line == "":
                continue
            else:
                yield [int(number) for number in line.split(" ") if number != ""]


def generate_boards(
    boards: Generator[List[int], None, None]
) -> Tuple[Iterator[Value], Iterator]:
    return (), (
        Value(board_index % 5, j, board_index // 5, number)
        for board_index, line in enumerate(boards)
        for j, number in enumerate(line)
    )


def cover_value(
    covered_values: Iterator, uncovered_values: Iterator[Value], call: int
) -> Tuple[Iterator[Value], Iterator[Value]]:
    new_uncovered, covered_this_round = partition(
        uncovered_values, lambda v: v.number == call
    )
    return itertools.chain(covered_this_round, covered_values), new_uncovered


def check_boards(covered_values: Iterator[Value]) -> Union[int, None]:
    """
    This function iterates over the list of covered values and checks if there's a marked column or row in a board. If
    there is, it returns the board; if not, return None
    :param covered_values:
    :return:
    """
    sorted_values = sorted(covered_values, key=lambda v: v.board)
    for board_index, board in itertools.groupby(sorted_values, lambda v: v.board):
        if check_all_lines(board):
            return board_index
    return None


def check_all_lines(value_stream: Iterator[Value]) -> bool:
    return any(
        map(
            lambda x: check_lines_in_one_direction(x[0], x[1]),
            zip(itertools.tee(value_stream), ("row", "col")),
        )
    )


def check_lines_in_one_direction(
    board_values: Iterator[Value], column_or_row: str
) -> bool:
    sorted_values = sorted(board_values, key=lambda v: getattr(v, column_or_row))
    for index, group in itertools.groupby(
        sorted_values, lambda v: getattr(v, column_or_row)
    ):
        if iterator_length(group) == 5:
            return True
    return False


def get_winning_board(
    covered: Iterator[Value],
    uncovered: Iterator[Union[None, Value]],
    bingo_calls: Iterator[int],
) -> Tuple[Iterator[Value], int]:
    this_call = next(bingo_calls)
    covered, uncovered = cover_value(covered, uncovered, this_call)
    check_covered, continue_covered = itertools.tee(covered)
    if (board_index := check_boards(check_covered)) is not None:
        return filter(lambda v: v.board == board_index, uncovered), this_call
    else:
        return get_winning_board(continue_covered, uncovered, bingo_calls)


def solve_bingo_part_one(data_stream: Generator[List[int], None, None]) -> int:
    bingo_calls = iter(next(data_stream))
    uncovered_winning_board, last_call = get_winning_board(
        *generate_boards(data_stream), bingo_calls=bingo_calls
    )
    return sum(map(lambda v: v.number, uncovered_winning_board)) * last_call

