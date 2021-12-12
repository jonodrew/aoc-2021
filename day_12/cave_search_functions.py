import functools
from typing import Dict, List, Iterator, Union, Tuple, FrozenSet

from day_12.classes import Cave
from helpers import combine_frozensets
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


def small_caves_to_duplicate(cave_data: Tuple[Cave, List[Cave]]) -> bool:
    cave, connections = cave_data
    return not (cave.big or cave.name in ("end", "start"))


def get_small_caves() -> Iterator[Tuple[Cave, List[Cave]]]:
    return filter(small_caves_to_duplicate, generate_all_connections(feed_input()).items())


def count_all_paths_when_visiting_one_small_twice():
    return len(functools.reduce(combine_frozensets, map(set_of_paths_when_visiting_one_small_twice, get_small_caves())))


def new_map_from_canon(cave_to_add: Tuple[Cave, List[Cave]]) -> Dict[Cave, List[Cave]]:
    small_cave, connections = cave_to_add
    small_cave = cave_prime(small_cave)
    prime_map = {**{connected_cave: [small_cave] for connected_cave in connections}, small_cave: connections}
    return combine_dicts(generate_all_connections(feed_input()), prime_map)


def set_of_paths_when_visiting_one_small_twice(small_cave: Tuple[Cave, List[Cave]]):
    this_map = new_map_from_canon(small_cave)
    all_paths = list(explore_every_path(this_map))
    replaced_paths = map(functools.partial(replace_prime_with_original, small_cave[0]), all_paths)
    return set_paths(map(stringify_path, replaced_paths))


def replace_prime_with_original(original: Cave, path: List[Cave]) -> Iterator[Cave]:
    return map(lambda cave: cave if cave != cave_prime(original) else original, path)


def stringify_path(path: List[Cave]) -> str:
    return ','.join((cave.name for cave in path))


def set_paths(all_string_paths: Iterator[str]) -> FrozenSet[str]:
    return frozenset(all_string_paths)


def cave_prime(cave: Cave) -> Cave:
    return Cave(name=f"{cave.name}-prime", big=cave.big)
