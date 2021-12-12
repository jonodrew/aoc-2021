import functools
from typing import Dict, List, Iterator, Union

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


@functools.lru_cache
def generate_all_connections(lines: Iterator[str]) -> Dict[Cave, List[Cave]]:
    return functools.reduce(combine_dicts, map(parse_line, lines))


def good_next_steps(all_onward_connections: List[Cave], visited: List[Cave]) -> Iterator[Cave]:
    return filter(lambda next_step: next_step.big or next_step not in visited, all_onward_connections)


def generate_new_path_and_step(cave_map: Dict[Cave, List[Cave]], current_step: Cave, visited: Union[None, List[Cave]]):
    return map(lambda step: (step, visited + [step]), good_next_steps(cave_map.get(current_step), visited))


def explore_every_path(cave_map: Dict[Cave, List[Cave]], current_step: Cave = Cave("start", False), visited: Union[None, List[Cave]] = None) -> Iterator[List[Cave]]:
    if visited is None:
        visited = [current_step]
    if current_step.name == "end":
        yield visited
    else:
        for step in good_next_steps(cave_map.get(current_step), visited):
            for path in explore_every_path(cave_map, step, visited + [step]):
                yield path
