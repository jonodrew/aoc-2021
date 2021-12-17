import dataclasses
import functools
import itertools
from typing import Iterator, FrozenSet, Tuple, Union


@dataclasses.dataclass(frozen=True)
class Packet:
    version: int
    type: int


@dataclasses.dataclass(frozen=True)
class LiteralValue(Packet):
    value: int


@dataclasses.dataclass(frozen=True)
class Operator(Packet):
    sub_packets: FrozenSet[Union[LiteralValue, 'Operator']]


def byte_size():
    return 4


def get_headers(packet: str, pointer: int) -> Tuple[int, int]:
    version_end = pointer + 3
    typed_end = version_end + 3
    return decode_three_letters(packet[pointer: version_end]), decode_three_letters(packet[version_end: typed_end])


def get_operator_length_var(packet: str, pointer: int, length_id: str) -> Tuple[int, int]:
    if length_id == "0":
        end_var_position = pointer + 15
    else:
        end_var_position = pointer + 11
    return int(packet[pointer: end_var_position], 2), end_var_position


def get_operator_callable(length_id: str, packet: str,
                          new_packets: Iterator[Union[None, Union[LiteralValue, Operator]]],
                          pointer: int):
    length_var, new_pointer = get_operator_length_var(packet, pointer, length_id)
    if length_id == "0":
        func = decode_for_length
    else:
        func = decode_for_count
    return functools.partial(func, length_var, packet, new_packets, new_pointer)


def decode_binary_packet(packet: str, pointer: int) -> Tuple[Union[LiteralValue, Operator], int]:
    headers = version_id, type_id = get_headers(packet, pointer)
    pointer_after_headers = pointer + 6
    if type_id == 4:
        decoded_packet, pointer_after_packet = decode_value_packet(packet, headers, pointer_after_headers)
    else:
        length_id = packet[pointer_after_headers]
        pointer_after_length = pointer_after_headers + len(length_id)
        operator_func = get_operator_callable(length_id, packet, iter([]), pointer_after_length)
        decoded_packet, pointer_after_packet = operator_func(headers)
    return decoded_packet, pointer_after_packet


def decode_for_count(count: int, packets: str, new_packets: Iterator[Union[LiteralValue, Operator]], pointer: int,
                     headers: Tuple[int, int]) -> Tuple[Operator, int]:
    if count == 0:
        return Operator(*headers, sub_packets=frozenset(new_packets)), pointer
    else:
        new_packet, pointer_position = decode_binary_packet(packets, pointer)
        return decode_for_count(count - 1, packets, itertools.chain(new_packets, [new_packet]),
                                pointer_position, headers)


def decode_for_length(length: int, packets: str, new_packets: Iterator[Union[LiteralValue, Operator]], pointer: int,
                      headers: Tuple[int, int]) -> Tuple[Operator, int]:
    if length == 0:
        return Operator(*headers, sub_packets=frozenset(new_packets)), pointer
    else:
        new_packet, pointer_position = decode_binary_packet(packets, pointer)
        packet_length = pointer_position - pointer
        return decode_for_length(length - packet_length, packets, itertools.chain(new_packets, [new_packet]),
                                 pointer_position, headers)


def decode_value_packet(packet: str, headers: Tuple[int, int], pointer: int = 6) -> Tuple[LiteralValue, int]:
    value, new_pointer = read_literal_value(packet, pointer)
    return LiteralValue(*headers, int(value, 2)), new_pointer


def decode_hex_to_binary(packet: str) -> str:
    return ''.join(map(lambda char: format(int(char, 16), "04b"), packet))


def decode_three_letters(version: str) -> int:
    padded = "0" + version
    return int(padded, 2)


def read_literal_value(value: str, indicator_var_pos: int) -> Tuple[str, int]:
    indicator_var = value[indicator_var_pos]
    word_start = indicator_var_pos + 1
    word_end = word_start + 4
    this_word = value[word_start: word_end]
    if indicator_var == "0":
        return this_word, word_end
    else:
        next_word, new_pointer = read_literal_value(value, word_end)
        return this_word + next_word, new_pointer


def calculate_version_sum(packet: Union[LiteralValue, Operator]) -> int:
    return sum(collect_version(packet))


def collect_version(packet: Union[LiteralValue, Operator], versions: FrozenSet = frozenset([])) -> FrozenSet[int]:
    versions = versions.union([packet.version])
    if isinstance(packet, LiteralValue):
        return versions
    else:
        return functools.reduce(lambda set_one, set_two: set_one.union(set_two), map(collect_version, iter(packet.sub_packets)), versions)


