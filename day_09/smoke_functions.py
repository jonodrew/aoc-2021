import functools
from typing import Tuple, List, Set, Iterator


def feed_data(file_path: str) -> Iterator[List[int]]:
    with open(file_path) as heights_grid_file:
        for line in heights_grid_file.readlines():
            yield [int(x) for x in line.strip()]


def get_neighbours(coordinates: Tuple[int, int], grid: List[List[int]]) -> List[int]:
    filter_func = functools.partial(check_on_map, len(grid), len(grid[0]))
    neighbour_coords = filter(filter_func, generate_neighbour_coords(coordinates))
    return [grid[y][x] for x, y in neighbour_coords]


def check_on_map(grid_height: int, grid_length: int, coords: Tuple[int, int]) -> bool:
    return grid_length > coords[0] >= 0 and grid_height > coords[1] >= 0


def generate_neighbour_coords(coordinates: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coordinates
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def is_local_minimum(coord: Tuple[int, int], grid: List[List[int]]) -> bool:
    neighbours = get_neighbours(coord, grid)
    value = grid[coord[1]][coord[0]]
    return all(map(lambda x: x > value, neighbours))


def find_minima(grid: List[List[int]]) -> Set[Tuple[int, int]]:
    all_coords = ((x, y) for x in range(len(grid[0])) for y in range(len(grid)))
    skip_coords = set()
    local_minima = set()
    for coord in filter(lambda next_coord: next_coord not in skip_coords, all_coords):
        if is_local_minimum(coord, grid):
            local_minima.add(coord)
            skip_coords.update(generate_neighbour_coords(coord))
    return local_minima


def calculate_total_risk_levels(grid: List[List[int]], minima: Set[Tuple[int, int]]) -> Iterator[int]:
    return sum(map(lambda x: 1 + x, (grid[y][x] for x, y in minima)))
