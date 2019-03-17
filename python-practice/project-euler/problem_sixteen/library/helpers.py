"""Helper functions to serve purposes."""

def print_(text: str) -> None:
    print(text)


def sum_string(text: str) -> int:
    try:
        return sum(map(int, text))
    except ValueError as e:
        print('Input value must be an integer!')
        raise e


if __name__ == '__main__':
    print_('Hello, world!')
