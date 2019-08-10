import numpy as np

import new_main


def test_find_max_run_for_index():
    mat = np.array(
        [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25],
        ]
    )
    # Left-diagonal
    received = new_main.find_max_run_for_index(mat, 1, 1, 4)
    expected = 43_225
    assert expected == received

    mat = np.array(
        [
            [25, 24, 23, 22, 21],
            [20, 19, 18, 17, 16],
            [15, 14, 13, 12, 11],
            [10, 9, 8, 7, 6],
            [5, 4, 3, 2, 1],
        ]
    )
    # Right
    received = new_main.find_max_run_for_index(mat, 1, 1, 4)
    expected = 93_024
    assert expected == received

    # Left-diagonal (left not calculated)
    received = new_main.find_max_run_for_index(mat, 0, 4, 4)
    expected = 21 * 17 * 13 * 9
    assert expected == received

    # Down
    received = new_main.find_max_run_for_index(mat, 0, 2, 4)
    expected = 23 * 18 * 13 * 8
    assert expected == received
