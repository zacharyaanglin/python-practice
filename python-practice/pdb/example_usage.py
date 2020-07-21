"""This is a broken library that will throw an error."""


def test():
    """Throw a NameError."""
    print(name_not_defined)

def test_2():
    """Throw an IndexError."""
    arr = [1, 2, 3]
    print(arr[3])
