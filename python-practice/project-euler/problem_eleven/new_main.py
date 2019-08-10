"""Solve Euler problem 11: https://projecteuler.net/problem=11"""

from dataclasses import dataclass
import itertools
from typing import Any, List, Optional, Tuple

import numpy as np

INPUT_FILE = "input.txt"


def find_max_run_for_index(mat: np.array, x: int, y: int, length: int = 4):
    """
    For a given matrix and x, y index, find the max product for length entries 
    in a given direction.
    """
    max_x, max_y = mat.shape
    # Left
    if y >= length - 1:
        left = mat[x, y] * mat[x, y - 1] * mat[x, y - 2] * mat[x, y - 3]
    else:
        left = 0

    # Right
    if y <= max_y - length:
        right = mat[x, y] * mat[x, y + 1] * mat[x, y + 2] * mat[x, y + 3]
    else:
        right = 0

    # Up
    if x >= length - 1:
        up = mat[x, y] * mat[x - 1, y] * mat[x - 2, y] * mat[x - 3, y]
    else:
        up = 0

    # Down
    if x <= max_x - length:
        _down = mat[x, y] * mat[x + 1, y] * mat[x + 2, y] * mat[x + 3, y]
    else:
        _down = 0

    # Right-Diagonal
    if x <= max_x - length and y <= max_y - length:
        right_diagonal = (
            mat[x, y] * mat[x + 1, y + 1] * mat[x + 2, y + 2] * mat[x + 3, y + 3]
        )
    else:
        right_diagonal = 0

    # Left-Diagonal
    if y >= length - 1 and x <= max_x - length:
        left_diagonal = (
            mat[x, y] * mat[x + 1, y - 1] * mat[x + 2, y - 2] * mat[x + 3, y - 3]
        )
    else:
        left_diagonal = 0

    return max(right, _down, right_diagonal, left_diagonal)


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        lines = file.readlines()

    num_lines = [[int(x) for x in line.split()] for line in lines]
    mat = np.array(num_lines)
    x_max, y_max = mat.shape

    max_prod = 0
    for x in range(x_max):
        for y in range(y_max):
            proposed_max = find_max_run_for_index(mat, x, y, 4)
            if proposed_max > max_prod:
                max_prod = proposed_max
    print(max_prod)
