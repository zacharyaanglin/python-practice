"""A solution to Project Euler problem 33."""
import datetime
import fractions
import functools
import itertools
import operator
from typing import Tuple

def remove_intersection_from_ints(i: int, j: int) -> Tuple[int, int]:
    set_i = set(str(i))
    set_j = set(str(j))
    intersection = set_i & set_j
    i_factored = int(''.join(set_i - intersection))
    j_factored = int(''.join(set_j - intersection))
    return i_factored, j_factored


def compare_factored_fractions(i: int, j: int) -> bool:
    i_factored, j_factored = remove_intersection_from_ints(i, j)
    return i/j == i_factored/j_factored


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    num_digits = 2
    start = 10**(num_digits - 1)
    end = 10**num_digits
    nums = range(start, end)
    filtered_nums = filter(lambda x: x % 10 != 0 and x % 11 != 0, nums)
    my_iter = itertools.combinations(filtered_nums, 2)  # 2 for numerator and denominator
    filtered_iter = filter(lambda x: len(set(str(x[0])) & set(str(x[1]))) == 1, my_iter)
    filtered_again = filter(lambda x: compare_factored_fractions(x[0], x[1]), filtered_iter)
    zipped = zip(*filtered_again)
    nums = next(zipped)
    numerator = functools.reduce(operator.mul, nums)
    dens = next(zipped)
    denominator = functools.reduce(operator.mul, dens)
    result = fractions.Fraction(numerator=numerator, denominator=denominator)
    print(result)
    print(datetime.datetime.now() - start_time)
