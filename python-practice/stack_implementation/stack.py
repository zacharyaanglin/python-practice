"""A stack implementation."""

from typing import Any


class Stack:
    def __init__(self):
        self._list = []

    def __len__(self) -> int:
        return len(self._list)

    def push(self, element: Any) -> None:
        """Push an element onto the top of the stack.

        Args:
            element: The thing to be added to the stack.

        Returns:
            None
        """
        self._list.append(element)

    def pop(self) -> Any:
        """Pop an element from the top of the stack.

        Returns:
            The top element on the stack.
        """
        if self._list:
            last_element = self._list[-1]
            self._list = self._list[:-1]
            return last_element
        else:
            return None
