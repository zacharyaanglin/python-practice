"""Solve Euler problem eighteen."""

import helpers

if __name__ == '__main__':
  with open('problem.txt') as file:
    lines = file.readlines()
    parsed_lines = [[int(i) for i in line.split()] for line in lines]
  
  the_tree = helpers.initialize_tree(parsed_lines)
  the_loaded_tree = helpers.load_tree(the_tree)
  print(the_loaded_tree[0][0].compute())
