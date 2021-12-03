import functools
import itertools
from typing import Generator, Callable, Iterator


def word_at_index(data_stream: Iterator[str], index: int) -> str:
    """
    This function iterates through an entire iterator of strings. It returns only the characters at position `index` as
    a new string
    :param data_stream:
    :param index:
    :return:
    """
    return "".join((word[index] for word in data_stream))


def commonest_bit(new_word: str, bit_if_equal: str = "1") -> str:
    """
    This function takes a binary word and finds the most common value. It does this with `.count`, a method for strings
    :param new_word:
    :param bit_if_equal:
    :return:
    """
    if new_word.count("0") == new_word.count("1"):
        return bit_if_equal
    else:
        return "0" if new_word.count("0") > new_word.count("1") else "1"


def least_common_bit(word: str) -> str:
    """
    This function returns the least common bit. This is done by finding the most common bit, and then flipping it
    :param word:
    :return:
    """
    return flip_bit(commonest_bit(word))


def flip_bit(bit: str) -> str:
    return "0" if bit == "1" else "1"


def generate_new_numbers(
    data_stream: Generator[str, None, None]
) -> Generator[str, None, None]:
    new_words = [[letter] for letter in data_stream.__next__()]
    for word in data_stream:
        for i, letter in enumerate(word):
            new_words[i].append(letter)
    for new_word in new_words:
        yield "".join(new_word)


def gamma_rate(data_stream: Generator[str, None, None]) -> str:
    return "".join(map(commonest_bit, generate_new_numbers(data_stream)))


def epsilon_rate(gamma_value: str) -> str:
    return "".join(map(flip_bit, gamma_value))


def solve_part_one(data_stream: Generator[str, None, None]) -> int:
    gamma_value = gamma_rate(data_stream)
    return int(gamma_value, 2) * int(epsilon_rate(gamma_value), 2)


def recursive_find_rating(
    words_to_search: Iterator[str],
    bit_to_find_function: Callable[[str], str],
    iteration: int = 0,
):
    old_words, check_words = itertools.tee(words_to_search, 2)
    bit_to_find = bit_to_find_function(word_at_index(old_words, iteration))
    new_words, check_words = itertools.tee(
        filter(lambda x: x[iteration] == bit_to_find, check_words)
    )
    list_check_words = list(check_words)
    if len(list_check_words) == 1:
        return list_check_words[0]
    iteration += 1
    return recursive_find_rating(new_words, bit_to_find_function, iteration)


def solve_part_two(data_stream: Generator[str, None, None]) -> int:
    o2_bit_function = functools.partial(commonest_bit, bit_if_equal="1")
    co2_bit_function = least_common_bit
    o2_words, co2_words = itertools.tee(data_stream)
    return int(recursive_find_rating(o2_words, o2_bit_function), 2) * int(
        recursive_find_rating(co2_words, co2_bit_function), 2
    )
