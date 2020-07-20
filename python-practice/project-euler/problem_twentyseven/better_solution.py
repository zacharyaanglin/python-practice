from sympy.ntheory import primerange
from itertools import product

primes = set(primerange(1, 10000))
best = {'i': 0, 'a': 0, 'b': 0}

for a, b in product(range(-999,1000), primerange(-1000,1001)):
    i, poly = 0, lambda n: n**2 + a*n + b
    while poly(i) in primes: i += 1
    if i > best['i']: best = {'i': i, 'a': a, 'b': b}

print(best['a'] * best['b'])
