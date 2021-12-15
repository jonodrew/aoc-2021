import functools
import itertools
from typing import Dict, Tuple, Any, List, FrozenSet, Iterator, Callable


def grid_of_values(file_path: str) -> Dict[Tuple[int, int], int]:
    with open(file_path) as grid_file:
        return {(int(x), int(y)): int(risk) for y, line in enumerate(grid_file.readlines()) for x, risk in enumerate(line.strip())}


def get_grid_length(grid: Dict[Tuple[int, int], Any]) -> int:
    return max(map(lambda coords: coords[0], grid.keys()))


def get_grid_height(grid: Dict[Tuple[int, int], Any]) -> int:
    return max(map(lambda coords: coords[1], grid.keys()))


def get_grid_size(grid: Dict[Tuple[int, int], Any]) -> Tuple[int, int]:
    return get_grid_length(grid), get_grid_height(grid)


def get_neighbour_coords(coords: Tuple[int, int], grid_height: int, grid_length: int) -> FrozenSet[Tuple[int, int]]:
    x, y = coords
    return frozenset(filter(lambda new_coords: new_coords != coords and coords_on_map(new_coords, grid_length, grid_height), itertools.product(range(x-1, x+2), range(y-1, y+2))))


def real_neighbour_coords(coords: Tuple[int, int],
                          theoretical_coord_func: Callable[[Tuple[int, int]], Iterator[Tuple[int, int]]],
                          grid_size: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    length, height = grid_size
    filter_func = functools.partial(coords_on_map, grid_length=length, grid_height=height)
    return filter(filter_func, theoretical_coord_func(coords))


def real_cardinal_coords(coords: Tuple[int, int], grid_size: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    return real_neighbour_coords(coords, theoretical_cardinal_neighbour_coords, grid_size)


def all_theoretical_neighbour_coords(coords: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x, y = coords
    return filter(lambda new_coords: new_coords != coords, itertools.product(range(x - 1, x + 2), range(y - 1, y + 2)))


def theoretical_cardinal_neighbour_coords(coords: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x, y = coords
    return filter(lambda new_coords: new_coords[0] == x or coords[1] == y, all_theoretical_neighbour_coords(coords))


def coords_on_map(coords: Tuple[int, int], grid_length: int, grid_height: int) -> bool:
    return all([0 <= coords[0] <= grid_length, 0 <= coords[1] <= grid_height])
