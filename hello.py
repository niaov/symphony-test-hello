"""Minimal module for Symphony verification testing.

Contains basic arithmetic functions. Codex agent will be asked to extend this
(e.g. add a multiply function) via a GitHub issue, then create a PR.
"""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def power(base: float, exponent: int) -> float:
    """Return base raised to the power of exponent.

    Handles the standard edge cases:
    - Any number (including 0) to the power 0 is 1.
    - A negative exponent returns the reciprocal of the positive power.
    """
    return base**exponent


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
