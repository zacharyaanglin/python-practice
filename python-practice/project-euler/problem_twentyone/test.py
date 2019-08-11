import main


def test_gather_proper_divisors():
    num = 64
    expected = {32, 16, 8, 4, 2, 1}
    received = set(main.gather_proper_divisors(num))
    assert expected == received

    num = 220
    expected = {1, 2, 4, 5, 10, 11, 20, 22, 44, 55, 110}
    received = set(main.gather_proper_divisors(num))
    assert expected == received

    num = 60
    expected = {30, 20, 15, 12, 10, 6, 5, 4, 3, 2, 1}
    received = set(main.gather_proper_divisors(num))
    assert expected == received
