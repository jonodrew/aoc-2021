import dataclasses
import functools
import itertools
import re
from typing import Iterator, Callable, Tuple

from day_05.vent_functions import Point


def feed_input(file_path: str = "./day_13/data.txt") -> Iterator[str]:
    with open(file_path) as points_file:
        return filter(lambda line: line != '', map(lambda line: line.strip(), points_file.readlines()))


def grid_of_dots(feed_func: Callable[[], Iterator[str]] = feed_input) -> Iterator[Point]:
    return map(lambda points_list: Point(*points_list), map(lambda int_list: map(int, int_list), map(lambda line: line.split(","), filter(lambda feed_line: not feed_line.startswith("f"), feed_func()))))


def instructions(feed_func: Callable[[], Iterator[str]] = feed_input) -> Iterator[str]:
    return map(lambda line: re.search(r"[xy]=\d*", line).group(), filter(lambda feed_line: feed_line.startswith("f"), feed_func()))


def reflect_point_in_line(instruction: Tuple[str, int], old_point: Point) -> Tuple[Point, Point]:
    direction, location = instruction
    delta = location - getattr(old_point, direction)
    reflected_point = Point(location + delta, old_point.y) if direction == "x" else Point(old_point.x, location + delta)
    return old_point, reflected_point


def empty_gen():
    yield from ()


def reflect_all_points_in_line(instruction: Tuple[str, int], old_dot_grid: Iterator[Point],
                               reflected_dots: Iterator[Point] = empty_gen()) -> Iterator[Point]:
    reflected_dots = list(reflected_dots)
    try:
        next_dot = next(old_dot_grid)
    except StopIteration:
        reflected_dots = list(reflected_dots)
        return reflected_dots
    new_points = reflect_point_in_line(instruction, next_dot)
    return reflect_all_points_in_line(instruction, old_dot_grid, itertools.chain(reflected_dots, new_points))


def fold_paper(instruction: str, dot_grid: Iterator[Point]) -> Iterator[Point]:
    direction, location = instruction_to_direction_location(instruction)
    all_points = functools.reduce(itertools.chain, map(functools.partial(reflect_point_in_line, (direction, location)), dot_grid))
    all_points = list(all_points)
    return iter(frozenset(filter(lambda point: getattr(point, direction) < location, all_points)))


def instruction_to_direction_location(instruction: str) -> Tuple[str, int]:
    split = instruction.split("=")
    return split[0], int(split[1])
