import main

def test_generate_numbers():
    start = 1
    offset = 2
    period = 4
    generator = main.generate_numbers(start=start, offset=offset, period=period)
    first_n = [next(generator) for _ in range(10)]
    assert first_n == [1, 3, 5, 7, 9, 13, 17, 21, 25, 31]


