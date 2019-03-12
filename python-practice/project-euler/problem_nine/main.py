"""https://projecteuler.net/problem=9

A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
a2 + b2 = c2

For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""

from functools import reduce
import math
from operator import mul
from typing import Optional, Tuple

def find_pythagorean_triple(sum: int) -> Optional[Tuple[int, int, int]]:
    """
    Find a Pythagorean triple (a, b, c) such that a + b + c = 1000.

    If no such triple exists, return None.
    """
    for a in range(1, int(sum/3)):
        for b in range(1, int(sum-2*a)):
            if a + b == sum/2 + (a*b) / sum:
                print('A is {}, B is {}'.format(a, b))
                return a, b, int(math.sqrt(a**2 + b**2))
    return None

if __name__ == '__main__':
    triple = find_pythagorean_triple(1_000)
    product = reduce(mul, triple)
    print('Triple is', triple)
    print('Product is', product)
    