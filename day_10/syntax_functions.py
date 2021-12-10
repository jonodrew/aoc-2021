import functools
import itertools
import statistics
from typing import List, Union, Iterator, Callable


def feed_input() -> Iterator[str]:
    with open("/Users/jonathankerr/projects/aoc-2021/day_10/data.txt", "r") as syntax_file:
        for line in syntax_file.readlines():
            yield line.strip()


def find_first_incorrect_closer_or_complete(line: Iterator[str], opening_list: List[Union[None, str]] = []) -> str:
    pairs = {"{": "}", "[": "]", "(": ")", "<": ">"}
    try:
        next_char = next(line)
    except StopIteration:
        return ''.join(map(lambda char: pairs.get(char), reversed(opening_list)))
    if next_char in pairs.keys():
        opening_list.append(next_char)
    else:
        last_opener = opening_list.pop()
        if pairs.get(last_opener) != next_char:
            return next_char
    return find_first_incorrect_closer_or_complete(line, opening_list)


def get_all_incorrect_closers_or_completers(input_func: Callable[[], Iterator[str]]) -> Iterator[str]:
    return map(lambda line: find_first_incorrect_closer_or_complete(line, []), map(iter, input_func()))


def finder_generator():
    return functools.partial(find_first_incorrect_closer_or_complete, [])


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


def score(input_func: Callable[[], List[str]], calc_score_func: Callable[[int, str], int], filter_func: Callable[[str], bool]) -> int:
    score_lines = filter(filter_func, get_all_incorrect_closers_or_completers(input_func))
    return functools.reduce(calc_score_func, score_lines, 0)

