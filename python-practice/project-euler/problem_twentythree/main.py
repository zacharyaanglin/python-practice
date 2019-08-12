"""Solve Euler problem 23: https://projecteuler.net/problem=23"""
from typing import List

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


if __name__ == "__main__":
    abundant_numbers = [i for i in range(1, 28123) if is_abundant(i)]
    print(abundant_numbers)
