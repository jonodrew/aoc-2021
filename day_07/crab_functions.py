import functools
from typing import Iterator, Callable

from day_06.fish_functions import generate_day_zero_fish


def generate_initial_positions() -> Iterator[int]:
    return iter(sorted(generate_day_zero_fish("/Users/jonathankerr/projects/aoc-2021/day_07/data.txt")))


def absolute_distance(final_point: int, current_point: int) -> int:
    return abs(current_point - final_point)


def exponential_distance(final_point: int, current_point: int) -> int:
    distance = absolute_distance(final_point, current_point)
    return int((distance * (distance + 1)) / 2)


def calculate_total_fuel_for_point(distance_func: Callable[[int, int], int], final_position: int,
                                   initial_positions: Iterator[int]) -> int:
    return sum(map(functools.partial(distance_func, final_position), initial_positions))


def generate_all_fuel_totals(initial_position_generator: Callable[[], Iterator[int]], exponential=False):
    range_of_positions = range(min(initial_position_generator()), max(initial_position_generator()) + 1)
    distance_funcs = {True: exponential_distance, False: absolute_distance}
    for total in (calculate_total_fuel_for_point(distance_funcs[exponential], position, initial_position_generator()) for position in range_of_positions):
        yield total


def calculate_minimum_fuel(initial_position_generator: Callable[[], Iterator[int]], exponential=False) -> int:
    all_totals = generate_all_fuel_totals(initial_position_generator, exponential)
    return minimum_of_curve(next(all_totals), all_totals)


def minimum_of_curve(current_total: int, totals: Iterator[int]) -> int:
    next_total = next(totals)
    if next_total > current_total:
        return current_total
    else:
        return minimum_of_curve(next_total, totals)
