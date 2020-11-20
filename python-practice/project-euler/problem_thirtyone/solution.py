"""
In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?
"""

import functools
import itertools


coins = {
    "1p": 0.01,
    "2p": 0.02,
    "5p": 0.05,
    "10p": 0.1,
    "20p": 0.2,
    "50p": 0.5,
    "£1": 1,
    "£2": 2,
}       


# Naive solution: 200 length permutations.
def naive():
    possible_answers = itertools.combinations_with_replacement(coins.values(), 200)
    possible_sums = (sum(ans) for ans in possible_answers)
    actual_sums = (total for total in possible_sums if total == 2)
    print(list(actual_sums))
    print(len(actual_sums))


@functools.lru_cache()
def dynamic(n: float) -> int:
    # Base case
    if n < 0.01:
        return 0
    if n == 0.01:
        return 1

    return dynamic(n - 0.01) + dynamic(n - 0.02) + dynamic(n - 0.05) + dynamic(n - 0.1) + dynamic(n - 0.2) + dynamic(n - 0.5) + dynamic(n - 1) + dynamic(n - 2)


def tabulation(n: float) -> int:
    solutions = {}
    
