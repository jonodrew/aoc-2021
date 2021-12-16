import dataclasses
import functools
import operator
import sys
from itertools import starmap
from typing import FrozenSet, Union, Dict, Tuple, List

from helpers.grid import real_neighbour_coords, theoretical_cardinal_neighbour_coords as neighbour_func, get_grid_size
from helpers.point import Point


@dataclasses.dataclass(frozen=True)
class Node(Point):
    risk: int


@dataclasses.dataclass(frozen=True)
class Edge:
    start_node: Node
    end_node: Node
    weight: int


def update_node(node_to_update: Node, new_values: Dict) -> Node:
    attributes = [attribute for attribute in dir(node_to_update) if not attribute.startswith("__")]
    return Node(**{key: new_values.get(key, getattr(node_to_update, key)) for key in attributes})


def next_step(shortest_path_tree_set: FrozenSet[Node], current_node: Node) -> Node:
    updated_shortest_path = shortest_path_tree_set.union({current_node})

    new_costed_steps = filter(lambda step: step not in updated_shortest_path, map(lambda child_node: update_node(child_node, {"cost": current_node.cost + child_node.risk}), current_node.children))
    return min(new_costed_steps, key=operator.attrgetter("cost"))


def update_node_with_children(node_coords: Tuple[int, int], node: Node, node_grid: Dict[Tuple[int, int], Node]) -> Node:
    node_neighbours = map(node_grid.get, real_neighbour_coords(node_coords, neighbour_func, get_grid_size(node_grid)))
    return update_node(node, {"children": frozenset(node_neighbours)})


def all_nodes_with_children(grid_of_risks: Dict[Tuple[int, int], int]) -> List[Node]:
    initial_grid = initial_grid_of_nodes(grid_of_risks)
    partial_update = functools.partial(update_node_with_children, node_grid=initial_grid)
    return list(starmap(partial_update, initial_grid.items()))


def initial_grid_of_nodes(grid_of_risks: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int], Node]:
    final_coords = get_grid_size(grid_of_risks)
    return {coords: Node(x=coords[0], y=coords[1], risk=value) for coords, value in grid_of_risks.items()}