import operator
from typing import List, FrozenSet, Union, Dict, Tuple

from helpers.graph import Node, update_node
from helpers.grid import real_cardinal_coords, get_grid_size, grid_of_values


def dijkstras_algorithm(current_node: Node, distances: Dict[Node, int],
                        risk_grid: Dict[Tuple[int, int], int],
                        to_visit: FrozenSet = frozenset(), path: FrozenSet = frozenset()):
    if current_node.final:
        return path
    else:
        updated_path = path.union({current_node})
        next_nodes_coords = real_cardinal_coords((current_node.x, current_node.y), get_grid_size(risk_grid))
        child_nodes = map(lambda next_coords: Node(*next_coords,
                                                   risk=risk_grid.get(next_coords),
                                                   cost=distances.get(current_node, 0) + risk_grid.get(next_coords),
                                                   final=True if next_coords == get_grid_size(risk_grid) else False), next_nodes_coords)
        to_visit = to_visit.union(filter(lambda node: node not in updated_path, child_nodes))
        next_node = min(to_visit, key=operator.attrgetter("cost"))
        to_visit = to_visit.difference(frozenset([next_node]))
        return dijkstras_algorithm(next_node, distances, risk_grid, to_visit, updated_path)


