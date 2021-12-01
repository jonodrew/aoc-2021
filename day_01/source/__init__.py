import itertools
from typing import Generator


def cast_data_to_int(datastream: Generator[int, None, None]):
    for datum in datastream:
        yield int(datum)


def compare_measurements(measurements: Generator[int, None, None]):
    previous_depth = measurements.__next__()
    larger_than_previous = 0
    for measurement in measurements:
        if measurement > previous_depth:
            larger_than_previous += 1
        previous_depth = measurement
    return larger_than_previous


def generate_three_measurements(data_generator: Generator[int, None, None]) -> Generator[int, None, None]:
    previous_window = iter((0, data_generator.__next__(), data_generator.__next__()))
    for value in data_generator:
        summable_window, current_window = itertools.tee(
            itertools.chain(itertools.islice(previous_window, 1, 3), [value]), 2)
        yield sum(summable_window)
        previous_window = current_window
