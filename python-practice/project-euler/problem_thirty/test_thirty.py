import thirty


def test_num_digits():
    assert thirty.num_digits(3) == ['3']
    assert thirty.num_digits(31) == ['3', '1']
    assert thirty.num_digits(415) == ['4', '1', '5']

