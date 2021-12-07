import functools
from typing import Iterator, Callable

from day_06.fish_functions import generate_day_zero_fish


def generate_initial_positions() -> Iterator[int]:
    return generate_day_zero_fish("/Users/jonathankerr/projects/aoc-2021/day_07/data.txt")


def absolute_distance(current_point: int, final_point: int) -> int:
    return abs(current_point - final_point)


def exponential_distance(current_point: int, final_point: int) -> int:
    distance = absolute_distance(current_point, final_point)
    return int((distance * (distance + 1)) / 2)


def calculate_total_fuel(initial_positions: Iterator[int], final_position: int, exponential: bool = False) -> int:
    distance_functions = {False: absolute_distance, True: exponential_distance}
    return sum(map(functools.partial(distance_functions[exponential], final_point=final_position), initial_positions))


def calculate_minimum_fuel_slowly(initial_position_generator: Callable[[], Iterator[int]], exponential=False):
    range_of_positions = range(min(initial_position_generator()), max(initial_position_generator()) + 1)
    return min(calculate_total_fuel(initial_position_generator(), position, exponential) for position in range_of_positions)

