"""Solve Project Euler problem 21: https://projecteuler.net/problem=21"""
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


def append_amicable_numbers(existing_list: List[int], num: int) -> List[int]:
    """If the number is amicable, append it and its pair to the list."""
    if num in existing_list:
        return list(set(existing_list))

    else:
        potential_friend = sum(gather_proper_divisors(num))

        # Perfect number
        if potential_friend == num:
            return list(set(existing_list))

        # Amicable number
        if sum(gather_proper_divisors(potential_friend)) == num:
            existing_list.extend([num, potential_friend])

        # Dedupe
        return list(set(existing_list))


if __name__ == "__main__":
    amicable_numbers: List[int] = []
    for i in range(1, 10_000):
        append_amicable_numbers(amicable_numbers, i)

    print(sum(list(set(amicable_numbers))))
