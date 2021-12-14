import functools
from typing import Iterator, Dict, Tuple, List

from helpers.immutable_dict import update_dict, combine_dicts
from more_itertools import sliding_window


def feed_input(file_path: str = "./day_14/data.txt") -> List[str]:
    with open(file_path) as points_file:
        return list(filter(lambda line: line != '', map(lambda line: line.strip(), points_file.readlines())))


def polymer_template() -> str:
    return feed_input()[0]


def pair_insertion_rules() -> Iterator[str]:
    yield from iter(feed_input()[1:])


def convert_rule_to_map(rule_map: Dict[Tuple[str, str], str], pair_insertion_rule: str) -> Dict[Tuple[str, str], str]:
    pair = tuple(pair_insertion_rule[0:2])
    element = pair_insertion_rule[-1]
    return update_dict(rule_map, pair, element)


def map_of_all_rules() -> Dict[Tuple[str, str], str]:
    return functools.reduce(convert_rule_to_map, pair_insertion_rules(), dict())


def get_new_element(window: Tuple[str, str]) -> str:
    return map_of_all_rules().get(window)


def polymer_pairs(polymer: Iterator[str]) -> Iterator[Tuple[str, str]]:
    return sliding_window(polymer, 2)


def new_dict_from_pair(old_pair_count: Tuple[Tuple[str, str], int]) -> Iterator[Dict[Tuple[str, str], int]]:
    pair, count = old_pair_count
    new_pairs = pair_from_rule(pair)
    return combine_dicts(*map(lambda new_pair: {new_pair: count}, new_pairs))


def convert_pair_map_to_char_count(char_map: Dict[Tuple[str, str], int], char_count: Dict[str, int]) -> Dict[str, int]:
    if not char_map:
        return add_trailing_char(char_count)
    else:
        pair, count = char_map.popitem()
        new_char_count = combine_dicts(char_count, {pair[0]: count})
        return convert_pair_map_to_char_count(char_map, new_char_count)


def add_trailing_char(char_map: Dict[str, int]) -> Dict[str, int]:
    trailing_char = polymer_template()[-1]
    return update_dict(char_map, trailing_char, 1)


def calculate_char_map(char_map: Dict[Tuple[str, str], int], steps: int) -> Dict[Tuple[str, str], int]:
    if steps == 0:
        return char_map
    else:
        new_char_map = functools.reduce(combine_dicts, map(new_dict_from_pair, char_map.items()), dict())
        return calculate_char_map(new_char_map, steps - 1)


def pair_from_rule(pair: Tuple[str, str]) -> Tuple[Tuple[str, str], Tuple[str, str]]:
    new_char = get_new_element(pair)
    return (pair[0], new_char), (new_char, pair[1])


def process_pair_map(steps: int) -> Dict[Tuple[str, str], int]:
    initial_char_map = {window: 1 for window in polymer_pairs(polymer_template())}
    return calculate_char_map(initial_char_map, steps)


def count_elements_after_steps(steps: int):
    processed_pair_map = process_pair_map(steps)
    return convert_pair_map_to_char_count(processed_pair_map, dict())


def subtract_least_common_element_from_most(steps: int) -> int:
    groups = count_elements_after_steps(steps)
    return max(groups.values()) - min(groups.values())
