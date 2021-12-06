import itertools
from dataclasses import dataclass
from typing import Tuple, Union, Generator, Iterator


@dataclass(frozen=True)
class LanternFish:
    time_to_spawn: int


def spawn(default_period: int = 6, rest_time: int = 2) -> Tuple[LanternFish, LanternFish]:
    return LanternFish(default_period), LanternFish(default_period + rest_time)


def age(fish: LanternFish) -> Tuple[LanternFish]:
    return LanternFish(fish.time_to_spawn - 1),


def process_single_fish(fish: LanternFish) -> Union[Tuple[LanternFish], Tuple[LanternFish, LanternFish]]:
    if fish.time_to_spawn == 0:
        return spawn()
    else:
        return age(fish)


def process_generation(generation: Generator[LanternFish, None, int]) -> Generator[LanternFish, None, int]:
    return fish_generator(itertools.chain(*map(process_single_fish, generation)))


def fish_generator(all_fish: Iterator[LanternFish]) -> Generator[LanternFish, None, int]:
    for fish in all_fish:
        yield fish
    return 1


def population_on_day(day_to_find: int, population: Generator[LanternFish, None, int]):
    if day_to_find == 0:
        return len(tuple(population))
    else:
        return population_on_day(day_to_find - 1, process_generation(population))


def generate_day_zero_fish(filepath: str) -> Iterator[LanternFish]:
    with open(filepath, "r") as fish_file:
        return map(LanternFish, (int(timer) for line in fish_file.read().splitlines() for timer in line.split(",")))
