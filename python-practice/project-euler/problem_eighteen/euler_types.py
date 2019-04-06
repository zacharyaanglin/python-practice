"""Types for Euler problem eighteen."""

from dataclasses import dataclass
from typing import Any

@dataclass
class EulerTree:
	value: int
	left: Any = None
	right: Any = None
	computed: bool = False
	max_val: int = 0

	def compute(self) -> float:
		"""Compute the correct path for this node."""
		if not self.left and not self.right:
			self.computed = True
			self.max_val = self.value
			return self.max_val
		
		if self.left and not self.left.computed:
			self.left.compute()
		
		if self.right and not self.right.computed:
			self.right.compute()
		
		self.max_val = self.value + max(self.left.max_val, self.right.max_val)
		return self.max_val
