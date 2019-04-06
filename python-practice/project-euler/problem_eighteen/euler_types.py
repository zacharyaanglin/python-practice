"""Types for Euler problem eighteen."""

from dataclasses import dataclass
from typing import Any

@dataclass
class EulerTree:
	left: Any
	right: Any
	value: int
