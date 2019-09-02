"""Solve Euler problem 26: https://projecteuler.net/problem=26"""
import decimal

PRECISION: int = 150


def get_long_string_fraction(numerator: int, denominator: int):
    """Turn a fraction into a decimal with lots of precision."""
    c = decimal.Context(prec=PRECISION)
    long_num = c.divide(numerator, denominator)
    return str(long_num)


def repeating_sequence(string: str):
    """Return the longest repeating sequence in a string."""
    for j in range(0, len(string)):
        substring = string[j:]
        for i in range(int(PRECISION / 2), 1, -1):
            if (
                substring[:i] * 2 == substring[: 2 * i]
                and substring[: int(i / 2)] * 2 != substring[:i]
            ):
                return substring[:i]
    return 1


if __name__ == "__main__":
    one_seventh = str(1 / 7)
    print(one_seventh)
    print(get_long_string_fraction(1, 7))
