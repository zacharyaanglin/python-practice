"""A script for generating Python triples with sum lower than N."""

import collections
import itertools
import math

import contexttimer
import typer


def triplets(limit: int):
    """Generate primitive triples according to Euclid's formula."""
    for m in range(2, int(limit)):
        for n in range(1, m):
            if m % 2 != n % 2 and math.gcd(m, n) == 1:
                a = m**2 - n**2
                b = 2 * m * n
                c = m**2 + n**2

            if a > limit:
                break

            yield(a, b, c)


def filter_trips(length: int):
    """Filter primitive triples to those with fitting perimeter."""
    triples = filter(lambda tup: sum(tup) <= length, triplets(length / 2))
    for trip in triples:
        yield trip


def expand_trips(length: int):
    """Expand triples to non-primitive."""
    triples = filter_trips(length)
    for trip in triples:
        for k in range(1, length):
            if k * sum(trip) > length:
                break
            yield tuple(k * i for i in trip)


def main(length: int):
    with contexttimer.Timer() as t:
        trips = [tuple(set(trip)) for trip in expand_trips(length)]
        deduped_trips = set(trips)
        counts = collections.Counter(sum(trip) for trip in deduped_trips)
        ind_counts = collections.Counter(counts.values())[1]
        print(ind_counts)
    print("Time elapsed:", t.elapsed)


if __name__ == "__main__":
    typer.run(main)
    
