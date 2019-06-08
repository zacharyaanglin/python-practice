"""Test the stack."""

from stack_implementation import stack


def test_stack():
    tested_stack = stack.Stack()
    tested_stack.push("first element")
    tested_stack.push("second element")
    tested_stack.push("third element")

    assert len(tested_stack) == 3
    last_element = tested_stack.pop()
    assert last_element == "third element"
    assert len(tested_stack) == 2
