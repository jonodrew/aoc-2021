import dataclasses
from typing import Self, Tuple, Union
from functools import partial

NumberPart = Union['Number', str]
NumberType = Tuple[NumberPart, NumberPart]


@dataclasses.dataclass(frozen=True)
class Number:
    left: NumberPart
    right: NumberPart

    def add(self, other: 'Number') -> Self:
        return Number(left=self, right=other)


def add(left: Number, right: Number) -> Number:
    return Number(left, right)


def lowest_form(proposed_number: Number) -> bool:
    return all(map(lambda part: isinstance(part, Number) or len(part) == 1, (proposed_number.left, proposed_number.right)))


def parse_number(snailfish_number: NumberPart) -> NumberPart:
    if len(snailfish_number) == 1:
        return snailfish_number
    number = snailfish_number[1:-1]
    if len(number) == 3:
        return Number(number[:1], number[-1])
    brackets = 0
    parts_dict = {'left': '', 'right': ''}
    parts = iter(["left", "right"])
    proposed_number_dict = {"left": None, "right": None}
    part = next(parts)
    for char in number:
        if char in {"[", "]"}:
            if char == "[":
                brackets += 1
            else:
                brackets -= 1
        elif char == ',' and brackets == 0:
            part = next(parts)
            continue
        parts_dict[part] += char
    proposed_number = Number(*map(parts_dict.get, ("left", "right")))
    if lowest_form(proposed_number):
        return proposed_number
    return Number(*map(parse_number, (proposed_number.left, proposed_number.right)))

