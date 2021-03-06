import itertools
from typing import Generator, Any, Tuple


def cast_data_to_int(
    datastream: Generator[str, None, None]
) -> Generator[int, None, None]:
    """
    This function takes a stream of strings and converts them into integers
    :param datastream:
    :return:
    """
    for datum in datastream:
        yield int(datum)


def multiply_and_zip_with_offset(
    generator: Generator[Any, None, None], copies: int
) -> Generator[Tuple[Any, Any, Any], None, None]:
    """
    This function takes a generator and clones it `copies` times. Then it zips the clones together with an offset of 1.
    For example, if the data_generator yielded (1, 2, 3, 4) and `copies` was 3, this would generate
    ((1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6))
    :param generator:
    :param copies:
    :return:
    """
    copies = itertools.tee(generator, copies)
    for zipped in zip(
        *(itertools.islice(copy, i, None, None) for i, copy in enumerate(copies))
    ):
        yield zipped


def compare_measurements(measurements: Generator[int, None, None]) -> int:
    """
    This function takes a stream of integers and duplicates it. Finally, it counts the number of times the second item
    in the tuple is larger than the first
    :param measurements:
    :return:
    """
    comparisons = multiply_and_zip_with_offset(measurements, 2)
    return len(
        [comparison for comparison in comparisons if comparison[1] > comparison[0]]
    )


def generate_three_measurements(
    data_generator: Generator[int, None, None]
) -> Generator[int, None, None]:
    """
    This function takes a stream of integers and copies it three times. It then zips them together with an offset of 1
    and 2 respectively, giving a tuple of three items. For example, if the data_generator yielded (1, 2, 3, 4) this
    would generate ((1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)). These tuples are summed and then yielded
    :param data_generator:
    :return:
    """
    windows = multiply_and_zip_with_offset(data_generator, 3)
    for window in windows:
        yield sum(window)
