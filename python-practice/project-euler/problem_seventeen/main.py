"""Solution to Euler problem seventeen."""
# pylint: disable=no-value-for-parameter

import click

import library.helpers as helpers


@click.command()
@click.option('--start', prompt='Start of series', type=int)
@click.option('--end', prompt='End of series', type=int)
def len_of_series(start: int, end:int) -> int:
    """Get the combined length of every word in a series from start to end."""
    answer = sum(map(helpers.len_of_number_word, range(start, end+1)))
    print(answer)
    return(answer)


if __name__ == '__main__':
    len_of_series()
