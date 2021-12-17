import pytest

from day_16.decoder import read_literal_value, Operator, LiteralValue, decode_hex_to_binary, decode_value_packet, \
    calculate_version_sum, decode_binary_packet, evaluate_operator


def test_read_literal_value():
    assert read_literal_value("101111111000101000", 0)[0] == "011111100101"


def test_decode_value_packet():
    packets, pointer = decode_value_packet("110100101111111000101000", headers=(6, 4))
    assert pointer == 21


@pytest.mark.parametrize(
    ["hex_word", "pointer_at_end", "output"], [
        ("38006F45291200", 49, Operator(1, 6, [LiteralValue(6, 4, 10), LiteralValue(2, 4, 20)])),
        ("D2FE28", 21, LiteralValue(6, 4, 2021)),
        ("EE00D40C823060", 51, Operator(7, 3, sub_packets=[
            LiteralValue(2, 4, 1), LiteralValue(4, 4, 2), LiteralValue(1, 4, 3),
        ]))
    ]
)
def test_recursively_decode_packet(hex_word, pointer_at_end, output):
    binary_packet = decode_hex_to_binary(hex_word)
    decoded_packet, pointer = decode_binary_packet(binary_packet, 0)
    assert decoded_packet == output
    assert pointer == pointer_at_end


@pytest.mark.parametrize(
    ["packets", "expected_sum"],
    [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31)
    ]
)
def test_calculate_version_sum(packets, expected_sum):
    packets, pointer = decode_binary_packet(decode_hex_to_binary(packets), 0)
    assert calculate_version_sum(packets) == expected_sum


@pytest.mark.parametrize(
    ["hex_word", "evaluation"],
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ]
)
def test_evaluate_operator(hex_word, evaluation):
    top_level_packet, pointer = decode_binary_packet(decode_hex_to_binary(hex_word))
    assert evaluate_operator(top_level_packet).value == evaluation
