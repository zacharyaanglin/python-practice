"""Solve Euler problem 25: https://projecteuler.net/problem=25"""

from functools import lru_cache


@lru_cache()
def fib(n: int):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


if __name__ == "__main__":
    ind = 1
    while True:
        if len(str(fib(ind))) == 1000:
            print(ind)
            break
        ind += 1
