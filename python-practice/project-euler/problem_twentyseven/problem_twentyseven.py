from typing import Tuple

import sympy


def isprime(n: int) -> bool:
    return sympy.isprime(n)


def consecutive_primes(a: int, b: int) -> Tuple[int]:
    vals = []
    n = 0
    while True:
        evaluation = n**2 + a * n + b
        if not isprime(evaluation):
            break
        vals.append(evaluation)
        n+=1
    return tuple(vals)


if __name__ == "__main__":
    num_primes = 0
    max_pair = (-999, -1000)
    for a in range(-999, 999):
        for b in range(-1000, 1000):
            temp_primes = consecutive_primes(a=a, b=b)
            if len(temp_primes) > num_primes:
                max_pair = (a, b)
                num_primes = len(temp_primes)

    print(f"Max pair: {max_pair}")
    print(f"Primes: {consecutive_primes(*max_pair)}")
