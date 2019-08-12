"""Solve Euler problem 22: https://projecteuler.net/problem=22"""
from functools import reduce
from operator import mul


def score_name(name: str) -> int:
    return sum(ord(char) - 64 for char in name)


if __name__ == "__main__":
    with open("p022_names.txt", "r") as file:
        names = file.read()
    names_list = names.replace('"', "").split(",")
    sorted_names = sorted(names_list)
    total = sum((ind + 1) * score_name(name) for ind, name in enumerate(sorted_names))

    print(total)
