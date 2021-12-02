import itertools
from functools import reduce
from typing import Tuple, Generator, Callable
import re
import operator


def parse_word_and_number(line: str) -> Tuple[str, int]:
    """
    This function will take a single string and return it as a tuple of a string and an int, assuming it has both in it
    :param line:
    :return:
    """
    re_match = re.match(r"(\w+) (\d+)", line)
    if re_match is not None:
        return re_match.group(1), int(re_match.group(2))
    else:
        raise ValueError


def translate_instruction(instruction: Tuple[str, int]) -> Tuple[int, int]:
    translation = {
        "forward": lambda x, y: (int(y), 0),
        "up": lambda x, y: (0, int(y) * -1),
        "down": lambda x, y: (0, int(y)),
    }
    return translation.get(instruction[0], lambda x, y: (x, y))(*instruction)


def calculate_position(
    current_position: Tuple[int, int, int], new_instruction: Tuple[int, int]
) -> Tuple[int, int, int]:
    return (
        current_position[0] + new_instruction[0],
        current_position[1] + new_instruction[1],
        0,
    )


def calculate_position_and_aim(
    current_position_and_aim: Tuple[int, int, int], new_instruction: Tuple[int, int]
) -> Tuple[int, int, int]:
    if new_instruction[0] == 0:
        return (
            current_position_and_aim[0],
            current_position_and_aim[1],
            current_position_and_aim[2] + new_instruction[1],
        )
    else:
        return (
            current_position_and_aim[0] + new_instruction[0],
            current_position_and_aim[1]
            + (current_position_and_aim[2] * new_instruction[0]),
            current_position_and_aim[2],
        )


def solve_part_two(data_stream: Generator[str, None, None]) -> int:
    return solve(data_stream, calculate_position_and_aim, (0, 0, 0))


def solve_part_one(data_stream: Generator[str, None, None]) -> int:
    return solve(data_stream, calculate_position, (0, 0, 0))


def solve(
    data_stream: Generator[str, None, None],
    position_function: Callable[
        [Tuple[int, int, int], Tuple[int, int]], Tuple[int, int, int]
    ],
    initial_position: Tuple[int, int, int],
):
    return operator.mul(
        *itertools.islice(
            reduce(
                position_function,
                map(translate_instruction, map(parse_word_and_number, data_stream)),
                initial_position,
            ),
            2,
        ),
    )
