import itertools
from typing import Generator


def cast_data_to_int(datastream: Generator[str, None, None]) -> Generator[int, None, None]:
    for datum in datastream:
        yield int(datum)


def compare_measurements(measurements: Generator[int, None, None]) -> int:
    first, second = itertools.tee(measurements, 2)
    comparisons = zip(first, itertools.islice(second, 1, None, None))
    return len([comparison for comparison in comparisons if comparison[1] > comparison[0]])


def generate_three_measurements(data_generator: Generator[int, None, None]) -> Generator[int, None, None]:
    first, second, third = itertools.tee(data_generator, 3)
    windows = zip(first, itertools.islice(second, 1, None, None), itertools.islice(third, 2, None, None))
    for window in windows:
        yield sum(window)
