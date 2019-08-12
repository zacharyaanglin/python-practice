"""Solve Euler problem 23: https://projecteuler.net/problem=23."""
from typing import List, Set

import numpy as np


def gather_proper_divisors(num: int) -> List[int]:
    root = np.sqrt(num)
    low_factors: List[int] = [
        i for i in range(1, int(np.floor(root)) + 1) if num % i == 0
    ]
    high_factors: List[int] = [int(num / i) for i in low_factors if i != 1]
    factors = low_factors + high_factors
    dedupe_factors = list(set(factors))

    return dedupe_factors


def is_abundant(num: int) -> bool:
    return sum(gather_proper_divisors(num)) > num


def can_be_sum_of_two_nums(num: int, num_list: List[int], num_set: Set[int]) -> bool:
    for x in num_list:
        if x > num_list[-1] / 2:
            return False
        elif num - x in num_set:
            return True
    return False


if __name__ == "__main__":
    abundant_numbers = [i for i in range(1, 28_123) if is_abundant(i)]
    abundant_set = set(abundant_numbers)
    print(
        sum(
            x
            for x in range(1, 28_123)
            if not can_be_sum_of_two_nums(x, abundant_numbers, abundant_set)
        )
    )
