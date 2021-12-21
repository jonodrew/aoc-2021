import dataclasses
import math
import operator
from functools import partial
from typing import Tuple, List, Iterator, FrozenSet


@dataclasses.dataclass(frozen=True)
class Scanner:
    name: str
    beacons: FrozenSet[Tuple[int, int, int]]
    abs_position: Tuple[int, int, int] = (0, 0, 0)


def feed_input(filepath: str = "./data.txt") -> Iterator[str]:
    with open(filepath, "r") as scanner_file:
        for line in scanner_file.readlines():
            yield line.strip()


def relative_distance(first_point: Tuple[int, int, int], second_point: Tuple[int, int, int]) -> float:
    subtracted_pairs = map(lambda pair: operator.sub(*pair), zip(first_point, second_point))
    squared_subtracted_pairs = map(lambda diff: diff**2, subtracted_pairs)
    return math.sqrt(sum(squared_subtracted_pairs))


def relative_distances(other_points: List[Tuple[int, int, int]], first_point: Tuple[int, int, int]) -> Iterator[float]:
    func = partial(relative_distance, first_point)
    yield from map(func, other_points)


def all_relative_distances(all_beacons: List[Tuple[int, int, int]]) -> Iterator[Iterator[float]]:
    yield from map(partial(relative_distances, all_beacons), all_beacons)


def assert_point_in_scanner_two_range(point_one_all_distances: FrozenSet[float], scanner_two_distances: Iterator[Iterator[float]]) -> bool:
    """
    If all the relative distances for one point are repeated for another point in space, then I am assuming they are the
    same point.
    :param point_one_all_distances:
    :param scanner_two_distances:
    :return:
    """
    try:
        relative_distances_to_this_point = next(scanner_two_distances)
    except StopIteration:
        return False
    if point_one_all_distances == frozenset(relative_distances_to_this_point):
        return True
    else:
        return assert_point_in_scanner_two_range(point_one_all_distances, scanner_two_distances)


def assert_overlapping(first_scanner_all_distances: Iterator[Iterator[float]],
                       second_scanner_output: List[tuple[int, int, int]], minimum: int = 12, current_count: int = 0) -> bool:
    """
    This assumes that two scanners overlap if `minimum`
    This function takes the output of the first scanner and the second scanner. For each set of distances in
    first_scanner_all_distances, it checks
    if any of those distances are in the relative distances of second_scanner_output. For every one that is, one is
    added to the count. At 12==`minimum`, the function returns True. If it runs out of comparisons before then, it
    returns False.
    :param first_scanner_all_distances:
    :param second_scanner_output:
    :param minimum:
    :param current_count:
    :return:
    """
    if current_count >= minimum:
        return True
    else:
        try:
            this_check = next(first_scanner_all_distances)
        except IndexError:
            return False
        if assert_point_in_scanner_two_range(frozenset(this_check), all_relative_distances(second_scanner_output)):
            updated_count = current_count + 1
        else:
            updated_count = current_count
    return assert_overlapping(first_scanner_all_distances, second_scanner_output, minimum, updated_count)
