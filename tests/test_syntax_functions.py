import pytest

from day_10.syntax_functions import find_first_incorrect_closer_or_complete, score_errors, score_autocomplete, \
    autocomplete_score_algorithm, get_all_incorrect_closers_or_completers


@pytest.fixture
def mock_input_func():
    def mock_input():
        lines = ['[({(<(())[]>[[{[]{<()<>>', '[(()[<>])]({[<{<<[]>>(', '{([(<{}[<>[]}>{[]{[(<()>',
                 '(((({<>}<{<{<>}{[]{[]{}', '[[<[([]))<([[{}[[()]]]', '[{[{({}]{}}([{[{{{}}([]',
                 '{<[[]]>}<{[{[{[]{()[[[]', '[<(<(<(<{}))><([]([]()', '<{([([[(<>()){}]>(<<{{',
                 '<{([{{}}[<[[[<>{}]]]>[]]']
        for line in lines:
            yield line

    return mock_input


@pytest.mark.parametrize(
    ["line", "expected"],
    [
        (['[', '(', '{', '(', '<', '(', '(', ')', ')', '[', ']', '>', '[', '[', '{', '[', ']', '{', '<', '(', ')', '<',
          '>', '>'], '}}]])})]'),
        (['{', '(', '[', '(', '<', '{', '}', '[', '<', '>', '[', ']', '}', '>', '{', '[', ']', '{', '[', '(', '<', '(',
          ')', '>'], "}"),
        (['[', '[', '<', '[', '(', '[', ']', ')', ')', '<', '(', '[', '[', '{', '}', '[', '[', '(', ')', ']', ']', ']'],
         ")")
    ]
)
def test_find_first_incorrect_closer(line, expected):
    assert ''.join(find_first_incorrect_closer_or_complete(iter(line))) == expected


def test_score_errors(mock_input_func):
    assert score_errors(mock_input_func) == 26397


def test_score_autocomplete(mock_input_func):
    assert score_autocomplete(mock_input_func) == 288957


@pytest.mark.parametrize(
    ["good_line", "expected"],
    [
        (['[', '(', '{', '(', '<', '(', '(', ')', ')', '[', ']', '>', '[', '[', '{', '[', ']', '{', '<', '(', ')', '<',
          '>', '>'], ['}', '}', ']', ']', ')', '}', ')', ']']),
        (['[', '(', '(', ')', '[', '<', '>', ']', ')', ']', '(', '{', '[', '<', '{', '<', '<', '[', ']', '>', '>', '('],
         [')', '}', '>', ']', '}', ')'])
    ]
)
def test_find_completing_closers(good_line, expected):
    assert list(find_first_incorrect_closer_or_complete(iter(good_line), [])) == expected


def test_autocomplete_score_algorithm(mock_input_func):
    assert autocomplete_score_algorithm(0, "])}>") == 294
