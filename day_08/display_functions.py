import functools
import itertools
from typing import Tuple, List, Iterator, Dict, Set

import helpers


def feed_input() -> Iterator[str]:
    with open("/Users/jonathankerr/projects/aoc-2021/day_08/data.txt", "r") as notes_file:
        for line in notes_file.readlines():
            yield line


def parse_line(line: str) -> Tuple[str, str]:
    split_line = line.split("|")
    return split_line.pop(0).strip(), split_line.pop(0).strip()


def parse_all_lines() -> Iterator[Tuple[str, str]]:
    return map(parse_line, feed_input())


def list_of_values(values_as_string: str) -> List[str]:
    return values_as_string.split(" ")


def tuple_of_list_of_values(values_tuple: Tuple[str, str]) -> Tuple[List[str], List[str]]:
    return list_of_values(values_tuple[0]), list_of_values(values_tuple[1])


def parse_input() -> Iterator[Tuple[List[str], List[str]]]:
    return map(tuple_of_list_of_values, parse_all_lines())


def display_iterator() -> Iterator[List[str]]:
    return map(lambda pair: pair[1], parse_input())


def signal_patterns_iterator() -> Iterator[List[str]]:
    for pair in parse_input():
        yield pair[0]


def count_ones_fours_sevens_eights() -> int:
    return helpers.iterator_length(filter(lambda x: len(x) in (2, 4, 3, 7), (word for display in display_iterator() for word in display)))


def calculate_mapping(current_mapping: Dict[int, Set[str]], number_to_define: str) -> Dict[int, Set[str]]:
    number_as_set = set(number_to_define)
    new_rules = {
        1: lambda x: len(x) == 2,
        7: lambda x: len(x) == 3,
        4: lambda x: len(x) == 4,
        8: lambda x: len(x) == 7,
        6: lambda x: len(x) == 6 and current_mapping[8] == number_as_set.union(current_mapping[7]),
        9: lambda x: len(x) == 6 and current_mapping[4].issubset(number_as_set),
        0: lambda x: len(x) == 6 and not(new_rules[6](x) or new_rules[9](x)),
        3: lambda x: len(x) == 5 and current_mapping[7].issubset(number_as_set),
        5: lambda x: len(x) == 5 and current_mapping[6].issuperset(number_as_set),
        2: lambda x: len(x) == 5 and not (new_rules[3](x) or new_rules[5](x)),
    }
    for value, rule in new_rules.items():
        if rule(number_to_define):
            new_mapping = {**current_mapping, **{value: number_as_set}}
            return new_mapping
    raise KeyError


def recursively_calculate_mapping(signal_line: Iterator[str], current_mapping: Dict[int, Set[str]]) -> Dict[int, Set[str]]:
    try:
        next_signal = next(signal_line)
    except StopIteration:
        return current_mapping
    try:
        current_mapping = calculate_mapping(current_mapping, next_signal)
    except KeyError:
        signal_line = itertools.chain(signal_line, [next_signal])
    return recursively_calculate_mapping(signal_line, current_mapping)


def decode_display(mapping: Dict[int, Set[str]], display: List[str]) -> str:
    display_sets = [set(value) for value in display]
    return ''.join(map(functools.partial(match_strokes, mapping), display_sets))


def match_strokes(mapping, display) -> str:
    return str(next(filter(lambda elem: elem[1] == display, mapping.items()))[0])


def find_all_mappings(all_signals: Iterator[List[str]]) -> Iterator[Dict[int, Set[str]]]:
    recursive_function = functools.partial(recursively_calculate_mapping, current_mapping={})
    return map(recursive_function, map(iter, all_signals))


def decode_all_displays():
    return map(decode_display, find_all_mappings(signal_patterns_iterator()), display_iterator())




