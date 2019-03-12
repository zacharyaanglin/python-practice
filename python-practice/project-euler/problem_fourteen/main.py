"""The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:
13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""

from functools import lru_cache


@lru_cache(10_000)
def collatz_length(num: int) -> int:
    count = 1
    if num < 2:
        return count
    return 1 + collatz_length(_collatz(num))


def _collatz(num: int) -> int:
    if num % 2 == 0:
        return num/2
    return 3 * num + 1


if __name__ == '__main__':
    max_len = 1
    temp_num = 0
    for i in range(500_000, 1_000_000):
        length = collatz_length(i)
        if length > max_len:
            max_len = length
            temp_num = i
        if i % 100_000 == 0:
            print(i)
    print(temp_num, max_len)
