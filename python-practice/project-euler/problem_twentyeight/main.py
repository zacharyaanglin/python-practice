import itertools

def generate_numbers(start: int, offset: int, period: int, stop=None):
    n = start
    initial_offset = offset
    yield n
    period_counter = 0
    while True:
        if stop is not None and n >= stop:
            break
        period_counter += 1
        n += offset
        yield n
        if period_counter == period:
            period_counter = 0
            offset += initial_offset

if __name__ == "__main__":
    print(sum(generate_numbers(start=1, offset=2, period=4, stop=1001**2)))
