"""Basic arithmetic helpers.

Every function accepts ``int`` or ``float`` values and rejects non-numeric
inputs (including booleans) with a descriptive :class:`TypeError`.
"""

from numbers import Real


def _validate_number(value: object, name: str) -> None:
    """Ensure *value* is a real number (int or float, not bool).

    Raises:
        TypeError: if *value* is not a real number.
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(
            f"Expected number for {name}, got {type(value).__name__}"
        )


def add(a: float, b: float) -> float:
    """Return the sum of two numbers.

    Args:
        a: First addend.
        b: Second addend.

    Returns:
        The sum of ``a`` and ``b``.

    Raises:
        TypeError: if either argument is not a real number.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers.

    Args:
        a: The minuend.
        b: The subtrahend.

    Returns:
        The result of ``a - b``.

    Raises:
        TypeError: if either argument is not a real number.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers.

    Args:
        a: First factor.
        b: Second factor.

    Returns:
        The product of ``a`` and ``b``.

    Raises:
        TypeError: if either argument is not a real number.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a * b


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
    print(f"7 - 4 = {subtract(7, 4)}")
    print(f"2 * 3 = {multiply(2, 3)}")
