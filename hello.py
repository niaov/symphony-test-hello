"""Minimal module for Symphony verification testing.

Contains basic arithmetic functions. Codex agent will be asked to extend this
(e.g. add a multiply function) via a GitHub issue, then create a PR.
"""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers.

    Args:
        a: The first addend.
        b: The second addend.

    Returns:
        The sum of ``a`` and ``b``.
    """
    return a + b


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
