import functools
from typing import Iterator, Callable

from day_06.fish_functions import generate_day_zero_fish


def generate_initial_positions() -> Iterator[int]:
    return generate_day_zero_fish("/Users/jonathankerr/projects/aoc-2021/day_07/data.txt")


def absolute_distance(current_point: int, final_point: int) -> int:
    return abs(current_point - final_point)


def square_distance(current_point: int, distance: int) -> int:
    return (current_point - distance)**2


def calculate_fuel(initial_positions: Iterator[int], final_position: int) -> int:
    return sum(map(functools.partial(absolute_distance, final_point=final_position), initial_positions))


def calculate_minimum_fuel_slowly(initial_position_generator: Callable[[], Iterator[int]]):
    range_of_positions = range(min(initial_position_generator()), max(initial_position_generator()) + 1)
    return min(calculate_fuel(initial_position_generator(), position) for position in range_of_positions)
