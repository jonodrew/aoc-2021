import functools
import itertools
import operator
from typing import Tuple, List, Iterator, FrozenSet, Callable

import helpers


def grid() -> Iterator[Iterator[int]]:
    with open(
            "/Users/jonathankerr/projects/aoc-2021/day_09/data.txt"
    ) as heights_grid_file:
        return ((int(x) for x in line.strip()) for line in heights_grid_file.readlines())


def get_value(grid_func: Callable[[], Iterator[Iterator[int]]], coords: Tuple[int, int]) -> int:
    return next((value for y, row in enumerate(grid_func()) for x, value in enumerate(row) if (x, y) == coords))


def grid_height(grid_func: Callable[[], Iterator[Iterator[int]]]) -> int:
    return helpers.iterator_length(grid_func())


def grid_length(grid_func: Callable[[], Iterator[Iterator[int]]]) -> int:
    return helpers.iterator_length(next(grid_func()))


def get_neighbour_values(coordinates: Tuple[int, int], grid_func: Callable[[], Iterator[Iterator[int]]]) -> Iterator[int]:
    return (get_value(grid_func, (x, y)) for x, y in generate_neighbour_coords(coordinates, grid_func))


def check_on_map(height: int, length: int, coords: Tuple[int, int]) -> bool:
    return length > coords[0] >= 0 and height > coords[1] >= 0


def generate_neighbour_coords(coordinates: Tuple[int, int], grid_func) -> Iterator[Tuple[int, int]]:
    x, y = coordinates
    return filter(functools.partial(check_on_map, grid_height(grid_func), grid_length(grid_func)), iter([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]))


def get_non_nine_neighbours(grid_func, coord: Tuple[int, int]) -> List[Tuple[int, int]]:
    filter_func = functools.partial(check_on_map, len(grid_func()), len(grid_func()[0]))
    neighbour_coords = filter(filter_func, generate_neighbour_coords(coord, grid_func))
    return list(
        filter(
            lambda new_coord: grid_func()[new_coord[1]][new_coord[0]] != 9, neighbour_coords
        )
    )


def is_local_minimum(grid_func, coord: Tuple[int, int]) -> bool:
    neighbours = get_neighbour_values(coord, grid_func)
    value = get_value(grid_func, coord)
    return all(map(lambda x: x > value, neighbours))


def find_minima(grid_func: Callable[[], Iterator[Iterator[int]]]) -> FrozenSet[Tuple[int, int]]:
    all_coords = itertools.product(range(grid_length(grid_func)), range(grid_height(grid_func)))
    skip_coords: FrozenSet = frozenset()
    local_minima: FrozenSet = frozenset()
    for coord in filter(lambda next_coord: next_coord not in skip_coords, all_coords):
        if is_local_minimum(grid_func, coord):
            local_minima = frozenset((*local_minima, coord))
            skip_coords = frozenset((*skip_coords, *generate_neighbour_coords(coord, grid_func)))
    return local_minima


def calculate_total_risk_levels(minima: FrozenSet[Tuple[int, int]], grid_func) -> int:
    return sum(map(lambda x: 1 + x, (grid_func()[y][x] for x, y in minima)))


def find_basin_size(grid_func, points_to_check: Iterator[Tuple[int, int]], basin_size: int = 0,
                    already_checked: FrozenSet = frozenset()) -> int:
    try:
        next_point = next(points_to_check)
    except StopIteration:
        return basin_size
    already_checked = frozenset((*already_checked, next_point))
    points_to_check = itertools.chain(
        points_to_check, iter(get_non_nine_neighbours(grid_func, next_point))
    )
    all_points = filter(
        functools.partial(next_coord_not_in_already_checked, already_checked),
        points_to_check,
    )
    return find_basin_size(grid_func, all_points, len(already_checked), already_checked)


@functools.lru_cache
def next_coord_not_in_already_checked(
        already_checked: FrozenSet, next_coord: Tuple[int, int]
) -> bool:
    return next_coord not in already_checked


def find_all_basin_sizes(grid_func: Callable) -> Iterator[int]:
    return map(functools.partial(find_basin_size, grid_func), map(lambda x: iter((x,)), find_minima(grid_func)))


def find_three_largest_and_get_product(grid_function=grid) -> int:
    return functools.reduce(
        operator.mul, sorted(find_all_basin_sizes(grid_function), reverse=True)[:3]
    )
