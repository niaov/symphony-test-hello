"""Minimal module for Symphony verification testing.

Contains basic arithmetic functions. Codex agent will be asked to extend this
(e.g. add a multiply function) via a GitHub issue, then create a PR.
"""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers.

    Boolean inputs are rejected even though bool is a subclass of int, because
    this function expects explicit numeric values rather than truth values.
    """
    for value in (a, b):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Expected number, got {type(value).__name__}")

    return a - b


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
