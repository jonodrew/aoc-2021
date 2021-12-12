import functools
from typing import Dict, List, Iterator

from day_12.classes import Cave
from helpers.immutable_dict import combine_dicts


def make_cave(cave_id: str) -> Cave:
    return Cave(cave_id, True if cave_id.isupper() else False)


def feed_input() -> Iterator[str]:
    with open("./day_12/data.txt") as cave_file:
        for line in cave_file.readlines():
            yield line.strip()


def parse_line(line: str) -> Dict[Cave, List[Cave]]:
    first_cave, second_cave = tuple(map(make_cave, line.split("-")))
    return {first_cave: [second_cave], second_cave: [first_cave]}


def generate_all_connections(lines: Iterator[str]) -> Dict[Cave, List[Cave]]:
    return functools.reduce(combine_dicts, map(parse_line, lines))
