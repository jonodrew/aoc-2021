import functools
import itertools
from typing import Iterator, Callable, Dict, Union, Tuple, List
from helpers.immutable_dict import update_dict
from more_itertools import sliding_window


def feed_input(file_path: str = "./day_14/data.txt") -> Iterator[str]:
    with open(file_path) as points_file:
        return filter(lambda line: line != '', map(lambda line: line.strip(), points_file.readlines()))


def polymer_template() -> str:
    return next(feed_input())


def pair_insertion_rules() -> Iterator[str]:
    yield from itertools.islice(feed_input(), 1, None)


def convert_rule_to_map(rule_map: Dict[str, str], pair_insertion_rule: str) -> Dict[str, str]:
    pair = pair_insertion_rule[0:2]
    element = pair_insertion_rule[-1]
    return update_dict(rule_map, pair, element)


@functools.lru_cache
def map_of_all_rules() -> Dict[str, str]:
    return functools.reduce(convert_rule_to_map, pair_insertion_rules(), dict())


@functools.lru_cache
def get_new_element(window: Tuple[str, str]) -> str:
    pair = ''.join(window)
    return map_of_all_rules().get(pair)


def insert_new_elements(polymer: str, new_elements: Iterator[str]) -> str:
    return "".join(old + new for old, new in itertools.zip_longest(polymer, new_elements, fillvalue=""))


def polymer_pairs(polymer: str) -> Iterator[Tuple[str, str]]:
    return sliding_window(polymer, 2)


def process_polymer(polymer: str, steps: int = 1) -> str:
    if steps == 0:
        return polymer
    else:
        new_elements = map(get_new_element, polymer_pairs(polymer))
        new_polymer = insert_new_elements(polymer, new_elements)
        return process_polymer(new_polymer, steps - 1)


def count_elements(polymer: str) -> List[Tuple[str, int]]:
    grouped_elems = itertools.groupby(sorted(polymer))
    elems_with_counts = map(lambda key_group: (key_group[0], len(list(key_group[1]))), grouped_elems)
    return sorted(elems_with_counts, reverse=True, key=lambda elem_tuple: elem_tuple[1])


def subtract_least_common_element_from_most(polymer: str) -> int:
    groups = count_elements(polymer)
    return groups[0][1] - groups[-1][1]
