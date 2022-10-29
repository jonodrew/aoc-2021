from pytest import mark

from day_17.snailfish import Number, parse_number


@mark.parametrize(
    ["example", "number"],
    [
        ("[1,2]", Number("1", "2")),
        ("[[1,2],3]", Number(Number("1", "2"), "3")),
        ("[9,[8,7]]", Number("9", Number("8", "7"))),
        ("[[1,9],[8,5]]", Number(Number("1", "9"), Number("8", "5"))),
        (
            "[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
            Number(
                left=Number(
                    left=Number(
                        left=Number(left="1", right="2"),
                        right=Number(left="3", right="4"),
                    ),
                    right=Number(
                        left=Number(left="5", right="6"),
                        right=Number(left="7", right="8"),
                    ),
                ),
                right="9",
            ),
        ),
    ],
)
def test_parse_number(example, number):
    assert parse_number(example) == number
