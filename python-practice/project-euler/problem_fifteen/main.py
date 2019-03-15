from math import factorial

def compute_n_grid_combinations(grid_width: int) -> int:
    numerator = factorial(grid_width * 2)
    denominator = factorial(grid_width) ** 2
    return numerator / denominator

if __name__ == '__main__':
    print(compute_n_grid_combinations(20))
    