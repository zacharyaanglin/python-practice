import click

from library.helpers import print_, sum_string


@click.command()
@click.option('-b', '--base', prompt='Base to raise', type=int)
@click.option('-p', '--power', prompt='Power to which the base should be raised', type=int)
def solve_problem_sixteen(base: int, power: str) -> None:
    """Solve Euler problem sixteen: sum the digits of an integer raised to an integer."""
    base_int, power_int = int(base), int(power)
    print_(sum_string(str(base_int ** power_int)))


if __name__ == '__main__':
    solve_problem_sixteen()
