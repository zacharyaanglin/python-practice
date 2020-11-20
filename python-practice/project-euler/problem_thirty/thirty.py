"""Find the sum of all the numbers that can be written as the sum of fifth powers of their digits."""

from typing import List


def num_digits(num: int) -> List[str]:
    return [char for char in str(num)]


def is_sum_of_fifth_powers(num: int):
    return sum(int(digit)**5 for digit in num_digits(num)) == num


nums = [i for i in range(9, 1_000_000) if is_sum_of_fifth_powers(i)]
print(nums)
print(sum(nums))

