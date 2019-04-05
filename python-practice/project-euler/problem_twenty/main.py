"""Solve problem twenty."""

import math

import click


@click.command()
@click.option('--num', default=100)
def main(num: int) -> None:
  """Sum the digits in a number factorialized."""
  click.echo(sum(int(i) for i in str(math.factorial(num))))


if __name__ == '__main__':
  main()
