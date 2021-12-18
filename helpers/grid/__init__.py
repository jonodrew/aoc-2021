import itertools
from typing import Iterator, Any, Dict, Tuple


def grid(cells: Iterator[Any], length: int) -> Dict[Tuple[int, int], Any]:
    new_dict = {}
    for y, chunk in enumerate(itertools.islice(cells, 0, None, length)):
        for x, value in enumerate(chunk):
            new_dict[(x, y)] = value
    return new_dict
