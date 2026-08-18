"""Minimal module for Symphony verification testing.

Contains basic arithmetic functions. Codex agent will be asked to extend this
(e.g. add a multiply function) via a GitHub issue, then create a PR.
"""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
