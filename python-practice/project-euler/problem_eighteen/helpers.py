"""Helper functions for Euler problem eighteen."""

from typing import List

import euler_types


def initialize_tree(input_list: List[List[str]]) -> List[List[euler_types.EulerTree]]:
  outer_list = []
  inner_list = []
  for row in input_list:
    for element in row:
      element = euler_types.EulerTree(value=int(element))
      inner_list.append(element)
    outer_list.append(inner_list)
    inner_list = []
  return outer_list


def load_tree(input_list: List[List[euler_types.EulerTree]]) -> euler_types.EulerTree:
  """Load an EulerTree from a list of lists of ints."""
  outer_list = []
  inner_list = []
  for idx, row in enumerate(input_list):
    if len(input_list) > idx + 1:
      for node_idx, node in enumerate(row):
        node.left = input_list[idx + 1][node_idx]
        node.right = input_list[idx + 1][node_idx + 1]
        inner_list.append(node)
      outer_list.append(inner_list)
      inner_list = []
  return outer_list
