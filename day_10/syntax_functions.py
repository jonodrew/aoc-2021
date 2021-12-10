import functools
import itertools
import statistics
from typing import List, Union, Iterator, Callable, Tuple


def feed_input() -> Iterator[str]:
    with open("/Users/jonathankerr/projects/aoc-2021/day_10/data.txt", "r") as syntax_file:
        for line in syntax_file.readlines():
            yield line.strip()


def find_first_incorrect_closer_or_complete(line: Iterator[str], opening_list: Tuple = ()) -> str:
    pairs = {"{": "}", "[": "]", "(": ")", "<": ">"}
    try:
        next_char = next(line)
    except StopIteration:
        return ''.join(map(lambda char: pairs.get(char), reversed(opening_list)))
    incorrect_char, new_opening = process_char(next_char, opening_list)
    if incorrect_char:
        return incorrect_char
    else:
        return find_first_incorrect_closer_or_complete(line, new_opening)


def process_char(char: str, opening_tuple: Tuple) -> Tuple[Union[str, None], Union[None, Tuple]]:
    pairs = {"{": "}", "[": "]", "(": ")", "<": ">"}
    if char in pairs.keys():
        new_opening_tuple = (*opening_tuple, char)
    else:
        last_opener = opening_tuple[-1]
        new_opening_tuple = opening_tuple[:-1]
        if pairs.get(last_opener) != char:
            return char, None
    return None, new_opening_tuple


def get_all_incorrect_closers_or_completers(input_func: Callable[[], Iterator[str]]) -> Iterator[str]:
    return map(find_first_incorrect_closer_or_complete, map(iter, input_func()))


def score_errors(input_func: Callable[[], List[str]]) -> int:
    return score(input_func, error_score_algorithm, lambda char: len(char) == 1)


def score_autocomplete(input_func: Callable[[], List[str]]) -> int:
    score_lines = list(filter(lambda char: len(char) > 1, get_all_incorrect_closers_or_completers(input_func)))
    return statistics.median(map(functools.partial(autocomplete_score_algorithm, 0), score_lines))


def autocomplete_score_algorithm(current_score: int, chars_to_score: str) -> int:
    score_dict = {")": 1, "]": 2, "}": 3, ">": 4}
    if not chars_to_score:
        return current_score
    else:
        current_char = chars_to_score[0]
        chars_to_score = chars_to_score[1:]
        current_score = current_score * 5 + score_dict.get(current_char)
    return autocomplete_score_algorithm(current_score, chars_to_score)


def error_score_algorithm(current_score: int, char_to_score: str) -> int:
    score_dict = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return current_score + score_dict.get(char_to_score, 0)


def score(input_func: Callable[[], List[str]], calc_score_func: Callable[[int, str], int],
          filter_func: Callable[[str], bool]) -> int:
    score_lines = filter(filter_func, get_all_incorrect_closers_or_completers(input_func))
    return functools.reduce(calc_score_func, score_lines, 0)
