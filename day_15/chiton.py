import dataclasses
import functools
import heapq
import math
import sys
from typing import Dict, Tuple, List

from day_09.smoke_functions import check_on_map


@dataclasses.dataclass(frozen=True)
class Node:
    coords: Tuple[int, int]
    risk: int
    cost: int

    def __lt__(self, other):
        return self.cost < other.cost

    def __repr__(self):
        return f"Node at {self.coords} has cost {self.cost}"

    def __eq__(self, other):
        return self.coords == other.coords and self.risk == other.risk

    def __hash__(self):
        return hash((self.risk, self.coords))


@functools.lru_cache
def gen_reference_grid(file_path: str = "./day_15/data.txt"):
    with open(file_path) as grid_file:
        return {(x, y): int(value) for y, line in enumerate(grid_file.readlines()) for x, value in enumerate(line.strip())}


def value_from_grid(coords: Tuple[int, int]) -> int:
    scaled_coords = map(lambda coord: coord % math.sqrt(len(gen_reference_grid())), coords)
    return gen_reference_grid().get(tuple(scaled_coords))


def scale_risk_value(coords: Tuple[int, int]) -> int:
    scalar = sum(map(lambda coord: coord // grid_length(), coords))
    if (scaled_risk:=scalar + value_from_grid(coords)) > 9:
        return scaled_risk - 9
    else:
        return scaled_risk


def grid_length(grid=None):
    if grid is None:
        grid = gen_reference_grid()
    return math.sqrt(len(grid))


def cardinal_neighbours(coords: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = coords
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


def neighbour_coords(coords: Tuple[int, int], scalar: int) -> List[Tuple[int, int]]:
    return list(filter(functools.partial(check_on_map, scalar * grid_length(), scalar * grid_length()), cardinal_neighbours(coords)))


def get_neighbour_nodes(current_node: Node, scalar: int):
    return list(map(lambda coords: Node(coords, scale_risk_value(coords), current_node.cost + scale_risk_value(coords)), neighbour_coords(current_node.coords, scalar)))


def dijkstras_algorithm(reference_grid: Dict[Tuple[int, int], int], scalar=1):
    shortest_path = {}
    visited = set()
    current_node = Node((0, 0), scale_risk_value((0, 0)), 0)
    to_visit = []
    final_coords = tuple(map(lambda coord: int(scalar * grid_length(reference_grid)) - 1, max(reference_grid.keys())))
    while current_node.coords != final_coords:
        for neighbour_node in filter(lambda neighbour: neighbour not in visited, get_neighbour_nodes(current_node, scalar)):
            if neighbour_node.cost < shortest_path.get(neighbour_node, sys.maxsize):
                shortest_path[neighbour_node] = neighbour_node.cost
            if neighbour_node not in to_visit:
                heapq.heappush(to_visit, neighbour_node)
        visited.update({current_node})
        current_node = heapq.heappop(to_visit)
    return current_node

