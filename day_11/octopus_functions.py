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
    flashes: int = 0


def octo_grid(file_path: str = "/home/jonathan/projects/aoc-2021/day_11/data.txt") -> Iterator[Octopus]:
    with open(file_path) as octo_file:
        return (Octopus(x, y, int(level)) for y, line in enumerate(octo_file.readlines()) for x, level in enumerate(line.strip()))


def grid_max_index():
    return 9


def new_octopus_from_old(old_octopus: Octopus, features) -> Octopus:
    attributes = ("x", "y", "active", "flashes", "level")
    return Octopus(**{key: features.get(key, getattr(old_octopus, key)) for key in attributes})


def reset_to_active(old_octopus: Octopus) -> Octopus:
    return new_octopus_from_old(old_octopus, {"active": True})


def combine_dicts(first_dict: Dict[Tuple[int, int], int], second_dict: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], int]:
    combined_dict = {**first_dict, **second_dict}
    for key, value in combined_dict.items():
        if key in first_dict and key in second_dict:
            combined_dict[key] = first_dict[key] + second_dict[key]
    return combined_dict


def reduce_frozen_set_to_dict(impacted_dict: Union[None, Dict[Tuple[int, int], int]], impacted_frozenset: FrozenSet) -> Dict[Tuple[int, int], int]:
    new_impacted = {coords: 1 for coords in impacted_frozenset}
    if impacted_dict is None:
        return new_impacted
    else:
        return combine_dicts(new_impacted, impacted_dict)


def impacted_by_single_flash(current_impact: Union[Dict[Tuple[int, int], int], None], next_flasher: Octopus) -> Dict[Tuple[int, int], int]:
    this_impact = {neighbour: 1 for neighbour in get_neighbour_coords((next_flasher.x, next_flasher.y))}
    if current_impact is None:
        current_impact = dict()
    return combine_dicts(current_impact, this_impact)


def all_octopus_coords_impacted_by_flashers(current_flashers: Iterator[Octopus]) -> Dict[Tuple[int, int], int]:
    return functools.reduce(impacted_by_single_flash, current_flashers, None)


def increase_level_by_one(octopus: Octopus) -> Octopus:
    return new_octopus_from_old(octopus, {"level": octopus.level + 1})


def increase_all_octopus_levels_by_one(flat_grid: Iterator[Octopus]):
    return map(increase_level_by_one, flat_grid)


def process_octopus(octopus: Octopus) -> Tuple[Octopus, FrozenSet[Tuple[int, int]]]:
    if octopus.level > 9 and octopus.active:
        return new_octopus_from_old(octopus, {"active": False, "flashes": octopus.flashes + 1,
                                              "level": 0}), get_neighbour_coords((octopus.x, octopus.y))
    else:
        return octopus, frozenset()


def generate_new_octopuses_and_impacted_coords(old_octopuses: Iterator[Octopus]) -> Tuple[Iterator[Octopus], Iterator[FrozenSet[Tuple[int, int]]]]:
    return tuple(zip(*map(process_octopus, old_octopuses)))


def generate_new_octopuses_and_all_impacted(old_octopuses: Iterator[Octopus]) -> Tuple[Iterator[Octopus], Dict[Tuple[int, int], int]]:
    new_octos, impacted = generate_new_octopuses_and_impacted_coords(old_octopuses)
    return new_octos, functools.reduce(reduce_frozen_set_to_dict, impacted, None)


def apply_impact(impact_coords: Dict[Tuple[int, int], int], old_octopus: Octopus) -> Octopus:
    if old_octopus.active:
        return new_octopus_from_old(old_octopus,
                                    {"level": old_octopus.level + impact_coords.get((old_octopus.x, old_octopus.y), 0)})
    else:
        return old_octopus


def generate_new_octopuses_after_impacts(old_octopuses: Iterator[Octopus]) -> Iterator[Octopus]:
    new_octopuses, impacted_coords = generate_new_octopuses_and_all_impacted(old_octopuses)
    if not impacted_coords:
        return new_octopuses
    else:
        return generate_new_octopuses_after_impacts(map(functools.partial(apply_impact, impacted_coords), new_octopuses))


def recursively_process_flashes(old_octopuses: Iterator[Octopus]) -> Iterator[Octopus]:
    new_octos_check, new_octos_continue = itertools.tee(generate_new_octopuses_after_impacts(old_octopuses))
    if not any(map(lambda octo: octo.level > 9 and octo.active, new_octos_check)):
        return new_octos_continue
    else:
        return recursively_process_flashes(new_octos_continue)


def step(old_octopuses: Iterator[Octopus]):
    return map(reset_to_active, recursively_process_flashes(map(increase_level_by_one, old_octopuses)))


def step_n_times(n: int, old_octopuses: Iterator[Octopus]) -> Iterator[Octopus]:
    if n == 0:
        return old_octopuses
    else:
        return step_n_times(n-1, step(old_octopuses))


@functools.lru_cache
def get_neighbour_coords(coords: Tuple[int, int]) -> FrozenSet[Tuple[int, int]]:
    x, y = coords
    return frozenset(filter(lambda new_coords: new_coords != coords and coords_on_map(new_coords), itertools.product(range(x-1, x+2), range(y-1, y+2))))


def coords_on_map(coords: Tuple[int, int]) -> bool:
    return all(map(lambda coord: 0 <= coord <= grid_max_index(), coords))


def get_first_simultaneous_flash(old_octopuses: Iterator[Octopus], step_counter: int = 0) -> int:
    check_octopuses, continue_octopuses = itertools.tee(old_octopuses)
    if all(map(lambda octopus: octopus.level == 0, check_octopuses)):
        return step_counter
    else:
        return get_first_simultaneous_flash(step(continue_octopuses), step_counter + 1)
