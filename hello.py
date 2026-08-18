"""Minimal module for Symphony verification testing.

Contains basic arithmetic functions hardened for production use:

- Operands are validated to be real numbers (``int``, ``float``, or other
  ``numbers.Real`` types); ``bool`` is rejected explicitly because it is a
  subclass of ``int`` and is almost always a caller mistake here.
- Non-finite ``float`` operands (NaN or +/- infinity) are rejected so invalid
  results do not propagate silently through the application.
"""

from __future__ import annotations

import math
from numbers import Real

__all__ = ["add", "fibonacci"]


def _validate_real(value: object, name: str) -> Real:
    """Validate and return a real-number operand.

    Args:
        value: The operand to validate.
        name: The operand name, used in error messages.

    Returns:
        The validated operand, unchanged.

    Raises:
        TypeError: If ``value`` is not a real number, or is a ``bool``.
        ValueError: If ``value`` is a non-finite ``float`` (NaN or infinity).
    """
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(
            f"{name} must be a real number (int or float), "
            f"got {type(value).__name__}"
        )
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return value


def add(a: Real, b: Real) -> Real:
    """Return the sum of two real numbers.

    Args:
        a: The first addend.
        b: The second addend.

    Returns:
        The sum of ``a`` and ``b``.

    Raises:
        TypeError: If either operand is not a real number, or is a ``bool``.
        ValueError: If either operand is a non-finite ``float`` (NaN or
            infinity).
    """
    return _validate_real(a, "a") + _validate_real(b, "b")


def fibonacci(n: int) -> int:
    """Return the nth Fibonacci number.

    The sequence is defined as fibonacci(0) == 0, fibonacci(1) == 1, and
    fibonacci(n) == fibonacci(n - 1) + fibonacci(n - 2) for n >= 2.

    Args:
        n: The zero-based index of the Fibonacci number to compute. Must be a
            non-negative integer.

    Returns:
        The nth Fibonacci number.

    Raises:
        TypeError: If ``n`` is not an integer, or is a ``bool``.
        ValueError: If ``n`` is negative.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(
            f"n must be an integer, got {type(n).__name__}"
        )
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
    print(f"fibonacci(10) = {fibonacci(10)}")
