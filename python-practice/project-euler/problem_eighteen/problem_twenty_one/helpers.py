"""Helpers for problem 21."""

import functools
from typing import List


def find_divisors(num: int) -> List[int]:
    pass

def divisor_gen(n: int) -> int:
    factors = list(factorGenerator(n))
    nfactors = len(factors)
    f = [0] * nfactors
    while True:
        yield functools.reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range(nfactors)], 1)
        i = 0
        while True:
            f[i] += 1
            if f[i] <= factors[i][1]:
                break
            f[i] = 0
            i += 1
            if i >= nfactors:
                return
