import itertools
from typing import Generator


def cast_data_to_int(datastream: Generator[str, None, None]) -> Generator[int, None, None]:
    """
    This function takes a stream of strings and converts them into integers
    :param datastream:
    :return:
    """
    for datum in datastream:
        yield int(datum)


def compare_measurements(measurements: Generator[int, None, None]) -> int:
    """
    This function takes a stream of integers and duplicates it. Then it runs the two together with an offset of 1,
    producing a stream of tuples that can then be compared with each other. Finally, it counts the number of times the
    second item in the tuple is larger than the first
    :param measurements:
    :return:
    """
    first, second = itertools.tee(measurements, 2)
    comparisons = zip(first, itertools.islice(second, 1, None, None))
    return len([comparison for comparison in comparisons if comparison[1] > comparison[0]])


def generate_three_measurements(data_generator: Generator[int, None, None]) -> Generator[int, None, None]:
    """
    This function takes a stream of integers and copies it three times. It then zips them together with an offset of 1
    and 2 respectively, giving a tuple of three items. For example, if the data_generator yielded (1, 2, 3, 4) this
    would generate ((1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)). These tuples are summed and then yielded
    :param data_generator:
    :return:
    """
    first, second, third = itertools.tee(data_generator, 3)
    windows = zip(first, itertools.islice(second, 1, None, None), itertools.islice(third, 2, None, None))
    for window in windows:
        yield sum(window)
