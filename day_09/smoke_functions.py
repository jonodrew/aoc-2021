import functools
import itertools
import operator
from typing import Tuple, List, Iterator, FrozenSet


@functools.lru_cache
def grid() -> List[List[int]]:
    with open("/Users/jonathankerr/projects/aoc-2021/day_09/data.txt") as heights_grid_file:
        return [[int(x) for x in line.strip()] for line in heights_grid_file.readlines()]


@functools.lru_cache
def get_neighbours(coordinates: Tuple[int, int]) -> List[int]:
    filter_func = functools.partial(check_on_map, len(grid()), len(grid()[0]))
    neighbour_coords = filter(filter_func, generate_neighbour_coords(coordinates))
    return [grid()[y][x] for x, y in neighbour_coords]


@functools.lru_cache
def check_on_map(grid_height: int, grid_length: int, coords: Tuple[int, int]) -> bool:
    return grid_length > coords[0] >= 0 and grid_height > coords[1] >= 0


@functools.lru_cache
def generate_neighbour_coords(coordinates: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coordinates
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


@functools.lru_cache
def get_non_nine_neighbours(coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    filter_func = functools.partial(check_on_map, len(grid()), len(grid()[0]))
    neighbour_coords = filter(filter_func, generate_neighbour_coords(coord))
    return list(filter(lambda new_coord: grid()[new_coord[1]][new_coord[0]] != 9, neighbour_coords))


def is_local_minimum(coord: Tuple[int, int]) -> bool:
    neighbours = get_neighbours(coord)
    value = grid()[coord[1]][coord[0]]
    return all(map(lambda x: x > value, neighbours))


def find_minima() -> FrozenSet[Tuple[int, int]]:
    all_coords = ((x, y) for x in range(len(grid()[0])) for y in range(len(grid())))
    skip_coords = frozenset()
    local_minima = frozenset()
    for coord in filter(lambda next_coord: next_coord not in skip_coords, all_coords):
        if is_local_minimum(coord):
            local_minima = frozenset((*local_minima, coord))
            skip_coords = frozenset((*skip_coords, *generate_neighbour_coords(coord)))
    return local_minima


def calculate_total_risk_levels(minima: FrozenSet[Tuple[int, int]]) -> Iterator[int]:
    return sum(map(lambda x: 1 + x, (grid()[y][x] for x, y in minima)))


def find_basin_size(points_to_check: Iterator[Tuple[int, int]], basin_size: int = 0, already_checked: FrozenSet = frozenset()) -> int:
    try:
        next_point = next(points_to_check)
    except StopIteration:
        return basin_size
    already_checked = already_checked.union(frozenset((next_point, )))
    points_to_check = itertools.chain(points_to_check, iter(get_non_nine_neighbours(next_point)))
    all_points = filter(functools.partial(next_coord_not_in_already_checked, already_checked), points_to_check)
    return find_basin_size(all_points, len(already_checked), already_checked)


@functools.lru_cache
def next_coord_not_in_already_checked(already_checked: FrozenSet, next_coord: Tuple[int, int]) -> bool:
    return next_coord not in already_checked


def find_all_basin_sizes() -> Iterator[int]:
    return map(find_basin_size, map(lambda x: iter((x, )), find_minima()))


def find_three_largest_and_get_product() -> int:
    return functools.reduce(operator.mul, sorted(find_all_basin_sizes(), reverse=True)[:3])

