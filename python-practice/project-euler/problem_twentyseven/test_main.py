import problem_twentyseven


def test_isprime():
    assert problem_twentyseven.isprime(2)
    assert not problem_twentyseven.isprime(4)
    assert problem_twentyseven.isprime(11)
    assert problem_twentyseven.isprime(29)
    assert problem_twentyseven.isprime(31)
    assert not problem_twentyseven.isprime(51)


def test_find_consecutive_quadratic_primes():
    assert problem_twentyseven.consecutive_primes(a=1, b=1) == tuple()
    assert problem_twentyseven.consecutive_primes(a=1, b=2) == (2,)
