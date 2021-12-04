import itertools
from dataclasses import dataclass
from typing import Generator, List, Tuple, Iterator, Union

from helpers import stream_data, iterator_length


@dataclass
class Value:
    row: int
    col: int
    board: int
    number: int
    covered: bool = False


def parse_data(file_path) -> Iterator[List[int]]:
    for i, line in enumerate(stream_data(file_path)):
        if i == 0:
            yield [int(number) for number in line.split(",")]
        else:
            if line == "":
                continue
            else:
                yield [int(number) for number in line.split(" ") if number != ""]


def generate_boards(boards: Iterator[List[int]]) -> Iterator[Value]:
    """
    This function generates the five-by-five grids that form the bingo games
    :param boards:
    :return:
    """
    return (
        Value(board_index % 5, j, board_index // 5, number)
        for board_index, line in enumerate(boards)
        for j, number in enumerate(line)
    )


def cover_value(call: int, all_values: Iterator[Value]) -> Iterator[Value]:
    """
    This function iterates over every value in `all_values` and flips the `.covered` property to True
    :param call:
    :param all_values:
    :return:
    """
    return (
        Value(v.row, v.col, v.board, v.number, True) if v.number == call else v
        for v in all_values
    )


def check_lines_in_one_direction(
    board_values: Iterator[Value], column_or_row: str
) -> bool:
    """
    This function looks in one direction, either vertically or horizontally, and tries to find a line that is complete.
    If there are no lines, it returns False
    :param board_values:
    :param column_or_row:
    :return:
    """
    sorted_values = sorted(board_values, key=lambda v: getattr(v, column_or_row))
    for index, group in itertools.groupby(
        sorted_values, lambda v: getattr(v, column_or_row)
    ):
        if all(v.covered for v in group):
            return True
    return False


def check_all_lines(value_stream: Iterator[Value]) -> bool:
    """
    This function checks every line, in all directions, looking for a line that's complete. As long as there's one,
    `any` will return True
    :param value_stream:
    :return:
    """
    return any(
        map(
            lambda x: check_lines_in_one_direction(x[0], x[1]),
            zip(itertools.tee(value_stream), ("row", "col")),
        )
    )


def check_boards(all_values: Iterator[Value]) -> Iterator[Union[int, None]]:
    """
    This function iterates over the list of values and checks if there's a marked column or row in a board. If
    there is, it yields the board; if not, it yields None
    :param all_values:
    :return:
    """
    grouped_values: Iterator[Tuple[int, Iterator[Value]]] = itertools.groupby(
        sorted(all_values, key=lambda v: v.board), lambda v: v.board
    )
    for board_index, board in grouped_values:
        if check_all_lines(board):
            yield board_index
    yield None


def get_winning_board_index(
    bingo_calls: Iterator[int], all_values: Iterator[Value]
) -> Tuple[Iterator[Value], int, int]:
    """
    This function recursively seeks the first winning board and returns the full set of values, the index of the
    winning board, and the call that the board won on
    :param bingo_calls:
    :param all_values:
    :return:
    """
    this_call = next(bingo_calls)
    new_values, check_values = itertools.tee(cover_value(this_call, all_values))
    if (board_index := next(check_boards(check_values))) is not None:
        return new_values, board_index, this_call
    else:
        return get_winning_board_index(bingo_calls, new_values)


def clear_up(all_values: Iterator[Value]) -> Iterator[Value]:
    """
    This function sweeps through all the values and bins the boards that have been completed. This ensures that in any
    round, all successful boards are removed
    :param all_values:
    :return:
    """
    board_check, all_values = itertools.tee(all_values)
    complete_boards = set(check_boards(board_check))
    return filter(lambda v: v.board not in complete_boards, all_values)


def get_last_winning_board_index(
    bingo_calls: Iterator[int], all_values: Iterator[Value]
) -> Tuple[Iterator[Value], int, int]:
    final_values, board_index, last_call = get_winning_board_index(
        bingo_calls=bingo_calls, all_values=all_values
    )
    check_values, next_values = itertools.tee(final_values)
    if iterator_length(itertools.groupby(check_values, key=lambda v: v.board)) == 1:
        return next_values, board_index, last_call
    else:
        return get_last_winning_board_index(bingo_calls, clear_up(next_values))


def score(final_values: Iterator[Value], board_index: int, last_call: int) -> int:
    return (
        sum(
            map(
                lambda v: v.number,
                filter(
                    lambda v: v.board == board_index and not v.covered, final_values
                ),
            )
        )
        * last_call
    )


def solve_bingo_part_one(data_stream: Iterator[List[int]]) -> int:
    return score(
        *get_winning_board_index(iter(next(data_stream)), generate_boards(data_stream))
    )


def solve_bingo_part_two(data_stream: Iterator[List[int]]) -> int:
    return score(
        *get_last_winning_board_index(
            iter(next(data_stream)), generate_boards(data_stream)
        )
    )
