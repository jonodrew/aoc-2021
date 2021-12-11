import dataclasses
import functools
import itertools
from typing import Iterator, Tuple, Dict, Union, FrozenSet


@dataclasses.dataclass(frozen=True)
class Octopus:
    x: int
    y: int
    level: int
    active: bool = True


def octo_grid(file_path: str = "/home/jonathan/projects/aoc-2021/day_11/data.txt") -> Iterator[Octopus]:
    with open(file_path) as octo_file:
        return (Octopus(x, y, int(level)) for y, line in enumerate(octo_file.readlines()) for x, level in enumerate(line.strip()))


def grid_height():
    return 9


def grid_length():
    return grid_height()


def get_octopus(flat_grid: Iterator[Octopus], coords: Tuple[int, int]) -> Octopus:
    return next(filter(lambda octopus: (octopus.x, octopus.y) == coords, flat_grid))


def flashers(flat_grid: Iterator[Octopus]) -> Iterator[Octopus]:
    return filter(lambda octopus: octopus.level > 9 and octopus.active, flat_grid)


def impacted_by_single_flash(current_impact: Union[Dict[Tuple[int, int], int], None], next_flasher: Octopus) -> Dict[Tuple[int, int], int]:
    this_impact = {neighbour: 1 for neighbour in get_neighbour_coords((next_flasher.x, next_flasher.y))}
    if current_impact is None:
        current_impact = dict()
    return combine_dicts(current_impact, this_impact)


def all_octopus_coords_impacted_by_flashers(current_flashers: Iterator[Octopus]) -> Dict[Tuple[int, int], int]:
    return functools.reduce(impacted_by_single_flash, current_flashers, None)


def combine_dicts(first_dict: Dict[Tuple[int, int], int], second_dict: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], int]:
    combined_dict = {**first_dict, **second_dict}
    for key, value in combined_dict.items():
        if key in first_dict and key in second_dict:
            combined_dict[key] = first_dict[key] + second_dict[key]
    return combined_dict


def increase_by_one(octopus: Octopus) -> Octopus:
    return Octopus(octopus.x, octopus.y, octopus.level + 1, octopus.active)


def increase_all_by_one(flat_grid: Iterator[Octopus]):
    return map(increase_by_one, flat_grid)


def process_octopus(octopus: Octopus) -> Tuple[Octopus, FrozenSet[Tuple[int, int]]]:
    if octopus.level > 9:
        return Octopus(octopus.x, octopus.y, level=0, active=False), get_neighbour_coords((octopus.x, octopus.y))
    else:
        return octopus, frozenset()


def generate_new_octopuses_and_impacted_coords(old_octopuses: Iterator[Octopus]) -> Tuple[Iterator[Octopus], Iterator[FrozenSet[Tuple[int, int]]]]:
    return tuple(zip(*map(process_octopus, old_octopuses)))


def generate_new_octopuses_and_all_impacted(old_octopuses: Iterator[Octopus]) -> Tuple[Iterator[Octopus], Dict[Tuple[int, int], int]]:
    new_octos, impacted = generate_new_octopuses_and_impacted_coords(old_octopuses)
    return new_octos, functools.reduce(reduce_frozen_set_to_dict, impacted, None)


def apply_impact(impact_coords: Dict[Tuple[int, int], int], old_octopus: Octopus) -> Octopus:
    return Octopus(old_octopus.x, old_octopus.y, old_octopus.level + impact_coords.get((old_octopus.x, old_octopus.y), 0), old_octopus.active)


def generate_new_octopuses_after_impacts(old_octopuses: Iterator[Octopus]) -> Iterator[Octopus]:
    new_octos, impacted_coords = generate_new_octopuses_and_all_impacted(old_octopuses)
    return map(functools.partial(apply_impact, impacted_coords), new_octos)


def step(old_octopuses: Iterator[Octopus]):
    return recursively_process_flashes(map(increase_by_one, old_octopuses))


def recursively_process_flashes(old_octopuses: Iterator[Octopus]) -> Iterator[Octopus]:
    new_octos_check, new_octos_continue = itertools.tee(generate_new_octopuses_after_impacts(old_octopuses))
    if not any(map(lambda octo: octo.level > 9 and octo.active, new_octos_check)):
        return new_octos_continue
    else:
        return recursively_process_flashes(new_octos_continue)

def reduce_frozen_set_to_dict(impacted_dict: Union[None, Dict[Tuple[int, int], int]], impacted_frozenset: FrozenSet) -> Dict[Tuple[int, int], int]:
    new_impacted = {coords: 1 for coords in impacted_frozenset}
    if impacted_dict is None:
        return new_impacted
    else:
        return combine_dicts(new_impacted, impacted_dict)


@functools.lru_cache
def get_neighbour_coords(coords: Tuple[int, int]) -> FrozenSet[Tuple[int, int]]:
    x, y = coords
    return frozenset(filter(lambda new_coords: new_coords != coords and coords_on_map(new_coords), itertools.product(range(x-1, x+2), range(y-1, y+2))))


def coords_on_map(coords: Tuple[int, int]) -> bool:
    return 0 <= coords[0] <= grid_height() and grid_length() >= coords[1] >= 0
