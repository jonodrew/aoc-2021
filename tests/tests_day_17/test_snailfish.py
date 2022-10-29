from pytest import mark

from day_17.snailfish import Number, parse_number


@mark.parametrize(
    ["example", "number"],
    [
        ("[1,2]", Number("1", "2")),
        ("[[1,2],3]", Number(Number("1", "2"), "3"))
    ]
)
def test_parse_number(example, number):
    assert parse_number(example) == number
