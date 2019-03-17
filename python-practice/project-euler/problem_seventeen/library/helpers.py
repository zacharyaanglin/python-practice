"""Helper functions to solve problem seventeen."""
from typing import Dict

from library.constants import number_words


def translate_num_to_words(num: int, number_words: Dict[int, str] = number_words) -> str:
    """Translate an incoming number to its English written representation."""
    thousands = num // 1_000
    thousands_remainder = num % 1_000

    hundreds = thousands_remainder // 100
    hundreds_remainder = thousands_remainder % 100

    tens = hundreds_remainder // 10
    tens_remainder = hundreds_remainder % 10

    # Base case, included for consistency.
    ones = tens_remainder // 1
    ones_remainder = tens_remainder % 1

    thousands_word = number_words[thousands]
    hundreds_word = number_words[hundreds]
    tens_word = number_words[tens*10]
    ones_word = number_words[ones]

    hundreds_word += ' hundred' if hundreds_word else ''
    thousands_word += ' thousand' if thousands_word else ''

    if hundreds_word and (tens_word or ones_word):
        hundreds_word += ' and'

    if tens_word == 'ten' and ones_word:
        tens_word = number_words[tens * 10 + ones]
        ones_word = ''

    return('{} {} {} {}'.format(thousands_word, hundreds_word, tens_word, ones_word))


def len_of_number_word(number: int) -> int:
    """Get the length of a translated number, not inclusive of spaces."""
    number_word = translate_num_to_words(number)
    len_of_number = len_number(number_word)
    return len_of_number


def len_number(text: str) -> int:
    """Get the number of letters in a number, not including spaces."""
    number = ''.join(text.split())
    return len(number)
