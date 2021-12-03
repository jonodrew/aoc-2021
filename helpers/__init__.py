import os
from typing import Generator, Iterator, Any


def current_path(filename=__file__) -> str:
    pth, _ = os.path.split(os.path.abspath(filename))
    return pth


def stream_data(filepath) -> Generator[str, None, None]:
    path_to_data = filepath + "/data.txt"
    with open(path_to_data, "r") as data_file:
        lines = data_file.read().splitlines()
        for line in lines:
            yield line


def iterator_length(iterator_of_unknown_length: Iterator[Any]) -> int:
    try:
        next(iterator_of_unknown_length)
    except StopIteration:
        return 0
    return 1 + iterator_length(iterator_of_unknown_length)