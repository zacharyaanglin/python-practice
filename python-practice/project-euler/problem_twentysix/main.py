"""Solve Euler problem 26: https://projecteuler.net/problem=26"""
import decimal
import itertools

PRECISION: int = 5_000


def get_long_string_fraction(numerator: int, denominator: int):
    """Turn a fraction into a decimal with lots of precision."""
    c = decimal.Context(prec=PRECISION)
    long_num = c.divide(numerator, denominator)
    return str(long_num)


def repeating_sequence(string: str):
    sequence = _repeating_sequence(string)
    if sequence == (new_sequence := _repeating_sequence(sequence)):
        return sequence
    while new_sequence != sequence:
        sequence = new_sequence
        new_sequence = _repeating_sequence(sequence)

    return new_sequence
        

def _repeating_sequence(string: str):
    """Return the longest repeating sequence in a string."""
    for j in range(0, len(string)):
        substring = string[j:]
        for i in range(int(PRECISION / 2), 1, -1):
            if (
                substring[:i] * 2 == substring[: 2 * i]
                and substring[: int(i / 2)] * 2 != substring[:i]
            ):
                return substring[:i]
    
    if len(substring) > 1:
        return one_term_repeating_sequence(substring)
    
    if len(string) > 1 and string[-2] == substring:
        return one_term_repeating_sequence(string)
    return string


def one_term_repeating_sequence(string: str):
    """Find a one-term repeating sequence."""
    if string == "".join(itertools.repeat(string[-1], len(string))):
        return string[-1]

    return string


if __name__ == "__main__":
    one_seventh = str(1 / 7)
    print(one_seventh)
    print(get_long_string_fraction(1, 7))
