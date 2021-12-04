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
    covered: bool = False


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
) -> Iterator[Value]:
    return (
        Value(board_index % 5, j, board_index // 5, number)
        for board_index, line in enumerate(boards)
        for j, number in enumerate(line)
    )


def cover_value(call: int, all_values: [Iterator[Value]]) -> Iterator[Value]:
    return (Value(v.row, v.col, v.board, v.number, True) if v.number == call else v for v in all_values)


def check_boards(all_values: Iterator[Value]) -> Union[int, None]:
    """
    This function iterates over the list of values and checks if there's a marked column or row in a board. If
    there is, it returns the board; if not, return None
    :param all_values:
    :return:
    """
    sorted_values = sorted(all_values, key=lambda v: v.board)
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
        checks = itertools.tee(group)
        if iterator_length(checks[0]) == 5 and all(v.covered for v in checks[1]):
            return True
    return False


def get_winning_board_index(
    all_values: [Iterator[Value]],
    bingo_calls: Iterator[int],
) -> Tuple[Iterator[Value], int, int]:
    this_call = next(bingo_calls)
    new_values, check_values = itertools.tee(cover_value(this_call, all_values))
    if (board_index := check_boards(check_values)) is not None:
        return new_values, board_index, this_call
    else:
        return get_winning_board_index(new_values, bingo_calls)


def get_last_winning_board_index(all_values: Iterator[Value], bingo_calls: Iterator[int]) -> int:
    pass


def solve_bingo_part_one(data_stream: Generator[List[int], None, None]) -> int:
    bingo_calls = iter(next(data_stream))
    final_values, board_index, last_call = get_winning_board_index(
        generate_boards(data_stream), bingo_calls=bingo_calls
    )
    return sum(map(lambda v: v.number, filter(lambda v: v.board == board_index and not v.covered, final_values))) * last_call


def solve_bingo_part_two(data_stream: Generator[List[int], None, None]) -> int:
    pass


