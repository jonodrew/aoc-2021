import sys
from typing import FrozenSet, Dict, Tuple, Callable

from helpers.graph import Node
from helpers.grid import real_cardinal_coords
from helpers.immutable_dict import replace_value


def dijkstras_algorithm(current_node: Node, distances: Dict[Node, int],
                        risk_grid: Dict[Tuple[int, int], int],
                        grid_size: Callable[[], Tuple[int, int]],
                        closest_parents: Dict[Node, Node],
                        to_visit: FrozenSet = frozenset(), path: FrozenSet = frozenset()):
    if (current_node.x, current_node.y) == grid_size():
        return path, closest_parents, distances
    else:
        updated_path = path.union({current_node})
        next_nodes_coords = real_cardinal_coords((current_node.x, current_node.y), grid_size())
        child_nodes = filter(lambda node: node not in updated_path,
                             map(lambda next_coords: Node(*next_coords, risk=risk_grid.get(next_coords)), next_nodes_coords)
                             )
        children_costs = zip(map(lambda child_node: (child_node, child_node.risk + distances.get(current_node, 0)), child_nodes))
        # still_to_visit = list(to_visit) + list(*children_costs)
        to_visit = to_visit.union(*children_costs)
        # next_node, cost = sorted(still_to_visit, key=lambda t: t[1]).pop(0)
        next_node, cost = min(to_visit, key=lambda t: t[1])
        parents, distances = updated_parents_distances(next_node, current_node, cost, closest_parents, distances)
        to_visit = to_visit.difference(frozenset({(next_node, cost)}))
        return dijkstras_algorithm(next_node, distances, risk_grid, grid_size, parents, to_visit, updated_path)


def update_distances(distance_dict: Dict[Node, int], node: Node, new_cost: int) -> Dict[Node, int]:
    return replace_value(distance_dict, node, new_cost)


def update_closest_parents(parents_dict: Dict[Node, Node], new_node: Node, parent_node: Node):
    return replace_value(parents_dict, new_node, parent_node)


def updated_parents_distances(new_node: Node, parent_node: Node, cost_to_node, parents: Dict[Node, Node],
                              distances: Dict[Node, int]) -> Tuple[Dict[Node, Node], Dict[Node, int]]:
    if cost_to_node < distances.get(new_node, sys.maxsize):
        return replace_value(parents, new_node, parent_node), replace_value(distances, new_node, cost_to_node)
    else:
        return parents, distances


