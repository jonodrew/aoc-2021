import collections
import itertools
import re
from dataclasses import dataclass
from typing import Tuple, Iterator


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class LineSegment:
    start: Point
    end: Point


def change_in_y_and_x(line: LineSegment) -> Tuple[float, float]:
    return (line.end.y - line.start.y),  (line.end.x - line.start.x)


def feed_data(file_path, exclude_diagonals: bool = True) -> Iterator[LineSegment]:
    with open(file_path, "r") as vector_file:
        for line in vector_file.read().splitlines():
            line_segment = parse_datum(line)
            if exclude_diagonals:
                if vertical_or_horizontal(line_segment):
                    yield line_segment
            else:
                yield line_segment


def vertical_or_horizontal(line: LineSegment) -> bool:
    return line.start.x == line.end.x or line.start.y == line.end.y


def construct_line_segment_from_string_points(point_one: str, point_two: str) -> LineSegment:
    return LineSegment(*map(construct_point_from_string, (point_one, point_two)))


def construct_point_from_string(coords_string="") -> Point:
    return Point(*map(int, coords_string.split(",")))


def parse_datum(vector_line: str) -> LineSegment:
    groups = re.match(r"(\d+,\d+)\D+(\d+,\d+)", vector_line).groups()
    return construct_line_segment_from_string_points(*groups)


def generate_all_integer_points_on_line(line: LineSegment) -> Iterator[Point]:
    gradient = change_in_y_and_x(line)
    new_point = line.start
    while new_point != line.end:
        yield new_point
        new_point = get_next_point(new_point, gradient)
    yield line.end


def generate_all_points_on_grid(all_lines: Iterator[LineSegment]) -> Iterator[Point]:
    return itertools.chain(*map(generate_all_integer_points_on_line, all_lines))


def find_points_that_occur_multiple_times(all_points: Iterator):
    return len(list(filter(lambda x: x > 1, collections.Counter(all_points).values())))


def get_next_point(old_point: Point, gradient: Tuple[float, float]) -> Point:
    steps = map(get_next_step, gradient)
    return Point(y=old_point.y + next(steps), x=old_point.x + next(steps))


def deal_with_horizontal_or_vertical(old_point: Point, gradient: Tuple[float, float]) -> Point:
    direction = get_direction(gradient)
    y_delta, x_delta = gradient
    if y_delta == 0:  # horizontal
        return Point(x=old_point.x + direction, y=old_point.y)
    elif x_delta == 0:  # vertical
        return Point(x=old_point.x, y=old_point.y + direction)


def get_next_step(delta: float) -> float:
    try:
        step = delta // abs(delta)
    except ZeroDivisionError:
        step = 0
    return step


def get_direction(gradient: Tuple[float, float]) -> float:
    return sum(gradient) // abs(sum(gradient))


def change_x_and_y(old_point: Point, gradient: float) -> Point:
    return change_x(change_y(old_point, gradient), gradient)


def change_y(old_point: Point, gradient: float) -> Point:
    return Point(old_point.x, old_point.y + int(gradient))


def change_x(old_point: Point, gradient: float) -> Point:
    return Point(old_point.x + int(gradient), old_point.y)


def solve_part_one(file_path: str):
    return find_points_that_occur_multiple_times(generate_all_points_on_grid(feed_data(file_path)))


def solve_part_two(file_path: str):
    return find_points_that_occur_multiple_times(generate_all_points_on_grid(
        feed_data(file_path, exclude_diagonals=False)))
