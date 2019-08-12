import itertools

if __name__ == "__main__":
    permutations = list(itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 10))
    sorted_permutations = sorted(permutations)
    print(sorted_permutations[999_999])
