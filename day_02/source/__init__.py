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
    re_match = re.match(r'(\w+) (\d+)', line)
    return re_match.group(1), int(re_match.group(2))


def translate_instruction(instruction: Tuple[str, int]) -> Tuple[int, int]:
    translation = {
        "forward": lambda x, y: (int(y), 0),
        "up": lambda x, y: (0, int(y)*-1),
        "down": lambda x, y: (0, int(y))
    }
    return translation.get(instruction[0])(*instruction)


def calculate_position(current_position: Tuple[int, int], new_position: Tuple[int, int]) -> Tuple[int, int]:
    return current_position[0] + new_position[0], current_position[1] + new_position[1]


def solve(data_stream: Generator[str, None, None]) -> int:
    return operator.mul(*reduce(calculate_position, map(translate_instruction, map(parse_word_and_number, data_stream))))





