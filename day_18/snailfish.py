import dataclasses
from typing import Union, Iterator, Tuple


@dataclasses.dataclass(frozen=True)
class Number:
    x: Union[int, Tuple[int, int], 'Number']
    y: Union[int, Tuple[int, int], 'Number']
    depth: int


def snailfish_numbers(file_path: str = "./day_18/data.txt") -> Iterator[str]:
    with open(file_path, "r") as snailfish_homework:
        yield from (line.strip() for line in snailfish_homework.readlines())


def centre_of_snailfish_str(snailfish_str: str, position: int, open_list: Tuple = tuple()) -> int:
    if (current_char:=snailfish_str[position]) == "," and open_list == tuple("["):
        return position
    else:
        if current_char == "]":
            updated_open_list = open_list[:-1]
        elif current_char == "[":
            updated_open_list = open_list + tuple(current_char)
        else:
            updated_open_list = open_list
    return centre_of_snailfish_str(snailfish_str, position + 1, updated_open_list)


def check_elem(elem: Union[Tuple[int, int], int, Number]) -> bool:
    if isinstance(elem, Number):
        return False
    else:
        return isinstance(elem, int) or all(map(lambda half: isinstance(half, int), elem))


def convert_string_to_snailfish(string_element: str):
    if string_element.isdigit():
        return int(string_element)
    elif string_element.count("[") == 1:
        return tuple(map(lambda elem: int(elem), string_element[1:-1].split(",")))
    else:
        pass


def deepest_pair_check(to_check: Tuple[str]) -> bool:
    """
    Checks if the two elements in the number are either an integer or a snailfish number (a tuple of integers)
    :param to_check:
    :return:
    """

    return all(map(check_elem, (to_check.x, to_check.y)))


def create_number_from_string(snailfish_str: str, open_list: Tuple = tuple(), depth: int = 0) -> Number:
    centre_position = centre_of_snailfish_str(snailfish_str, 0, open_list)
    elements = snailfish_str[1:centre_position], snailfish_str[centre_position:-1]



