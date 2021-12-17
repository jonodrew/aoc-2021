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


def decode_binary_packet(packet: str) -> Tuple[Union[LiteralValue, Operator], int]:
    headers = version_id, type_id = (decode_three_letters(packet[:3]), decode_three_letters(packet[3:6]))
    if type_id == 4:
        packet, pointer = decode_value_packet(packet[6:], headers)
    else:
        length_id = packet[6]
        if length_id == "0":
            sub_packet_length = int(packet[7:22], 2)
            packet, pointer = decode_for_length(sub_packet_length, packet[22:], iter([]), headers), sub_packet_length
        else:
            sub_packet_count = int(packet[7:18], 2)
            packet, pointer = decode_for_count(sub_packet_count, packet[18:], iter([]), headers, 18)
    return packet, pointer


def decode_for_count(count: int, packets: str, new_packets: Iterator[Union[LiteralValue, Operator]], headers: Tuple[int, int], pointer: int = 0) -> Tuple[Operator, int]:
    if count == 0:
        return Operator(*headers, sub_packets=frozenset(new_packets)), pointer
    else:
        new_packet, new_pointer = decode_binary_packet(packets)
        return decode_for_count(count - 1, packets[new_pointer:], itertools.chain(new_packets, [new_packet]), headers, pointer + new_pointer)


def decode_for_length(length: int, packets: str, new_packets: Iterator[Union[LiteralValue, Operator]], headers: Tuple[int, int]) -> Operator:
    if length == 0:
        return Operator(*headers, sub_packets=frozenset(new_packets))
    else:
        new_packet, new_packet_length = decode_binary_packet(packets)
        return decode_for_length(length - new_packet_length, packets[new_packet_length:], itertools.chain(new_packets, [new_packet]),headers)


def decode_value_packet(packet: str, headers: Tuple[int, int], pointer: int = 6) -> Tuple[LiteralValue, int]:
    value, new_pointer = read_literal_value(packet, pointer)
    return LiteralValue(*headers, int(value, 2)), new_pointer


def decode_hex_to_binary(packet: str) -> str:
    return ''.join(map(lambda char: format(int(char, 16), "04b"), packet))


def decode_three_letters(version: str) -> int:
    padded = "0" + version
    return int(padded, 2)


def read_literal_value(value: str, pointer: int) -> Tuple[str, int]:
    pointer = pointer + 5
    if value.startswith("0"):
        return last_four_letters(value), pointer
    else:
        next_chunk = value[5:]
        new_chunk, new_pointer = read_literal_value(next_chunk, pointer)
        return last_four_letters(value) + new_chunk, new_pointer


def last_four_letters(chunk: str) -> str:
    return chunk[1:5]


def calculate_version_sum(packet: Union[LiteralValue, Operator]) -> int:
    return sum(collect_version(packet))


def collect_version(packet: Union[LiteralValue, Operator], versions: FrozenSet = frozenset([])) -> FrozenSet[int]:
    versions = versions.union([packet.version])
    if isinstance(packet, LiteralValue):
        return versions
    else:
        return functools.reduce(lambda set_one, set_two: set_one.union(set_two), map(collect_version, iter(packet.sub_packets)), versions)


