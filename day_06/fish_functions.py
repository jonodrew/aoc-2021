from typing import Iterator


def population_on_day(day_to_find: int, population: Iterator[int]):
    frequency_of_timers = map(tuple(population).count, (i for i in range(9)))
    return recursive_frequency(frequency_of_timers, day_to_find)


def recursive_frequency(old_frequency: Iterator[int], day_to_find: int) -> int:
    """
    This function recursively seeks the frequency at where the day == 0
    :param old_frequency:
    :param day_to_find:
    :return:
    """
    if day_to_find == 0:
        return sum(old_frequency)
    else:
        return recursive_frequency(move_along(old_frequency), day_to_find - 1)


def move_along(frequencies: Iterator[int]) -> Iterator[int]:
    """
    This moves every frequency along one, except the frequency of sixes - which is moved down but has the frequency of
    zeroes added to it. Finally, the function yields the frequency of zeroes - which is the new frequency of eights.
    This is because wherever there's a zero, there's (essentially) a new 6 and a new 8.
    :param frequencies:
    :return:
    """
    zeroes = next(frequencies)
    for i, frequency in enumerate(frequencies):
        if i == 6:
            yield zeroes + frequency
        else:
            yield frequency
    yield zeroes


def generate_day_zero_fish(filepath: str) -> Iterator[int]:
    with open(filepath, "r") as fish_file:
        return (int(timer) for line in fish_file.read().splitlines() for timer in line.split(","))
