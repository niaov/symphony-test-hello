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

__all__ = [
    "add",
    "calculate_discount",
    "cube",
    "factorial",
    "fibonacci",
    "greet",
    "is_even",
    "square",
]


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


def cube(n: float) -> float:
    """Return the cube of a real number.

    Args:
        n: The number to cube.

    Returns:
        The cube of ``n`` (``n * n * n``).

    Raises:
        TypeError: If ``n`` is not a real number, or is a ``bool``.
        ValueError: If ``n`` is a non-finite ``float`` (NaN or infinity).
    """
    n = _validate_real(n, "n")
    return n * n * n


def factorial(n: int) -> int:
    """Return the factorial of a non-negative integer.

    Args:
        n: The integer to compute the factorial of. Must be a non-negative
            integer.

    Returns:
        The factorial of ``n`` (``n!``), defined as the product of all
        positive integers up to and including ``n`` (``factorial(0) == 1``).

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
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def greet(name: str) -> str:
    """Return a greeting for the given name.

    Args:
        name: The name to greet.

    Returns:
        A greeting string such as ``"Hello, Alice!"``.

    Raises:
        TypeError: If ``name`` is empty or not a string.
    """
    if not isinstance(name, str) or not name:
        raise TypeError("name must be a non-empty string")
    return f"Hello, {name}!"


def calculate_discount(subtotal: Real, is_new_customer: bool) -> dict[str, Real]:
    """Calculate discounts, shipping, and total for a purchase.

    A single percentage discount tier applies based on the subtotal (the
    highest tier only; tiers do not stack). New customers receive an
    additional flat $5 discount that stacks after the percentage discount.
    Shipping is free for large orders or for new customers above the
    mid-tier threshold, otherwise it is a flat $10.

    Args:
        subtotal: The pre-discount purchase subtotal.
        is_new_customer: Whether the customer is new.

    Returns:
        A dict with keys ``subtotal``, ``discount_rate``,
        ``discount_amount``, ``new_customer_discount``, ``shipping``, and
        ``total``.

    Raises:
        TypeError: If ``subtotal`` is not a real number (or is a ``bool``),
            or if ``is_new_customer`` is not a ``bool``.
        ValueError: If ``subtotal`` is a non-finite ``float`` (NaN or
            infinity).
    """
    subtotal = _validate_real(subtotal, "subtotal")
    if not isinstance(is_new_customer, bool):
        raise TypeError(
            "is_new_customer must be a bool, "
            f"got {type(is_new_customer).__name__}"
        )

    if subtotal >= 200:
        discount_rate = 0.20
    elif subtotal >= 100:
        discount_rate = 0.10
    else:
        discount_rate = 0.0

    discount_amount = subtotal * discount_rate
    new_customer_discount = 5.0 if is_new_customer else 0.0

    if subtotal >= 200 or (is_new_customer and subtotal >= 100):
        shipping = 0.0
    else:
        shipping = 10.0

    total = subtotal - discount_amount - new_customer_discount + shipping
    return {
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount_amount": discount_amount,
        "new_customer_discount": new_customer_discount,
        "shipping": shipping,
        "total": total,
    }


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


def is_even(n: int) -> bool:
    """Return whether an integer is even.

    Args:
        n: The integer to check.

    Returns:
        True if ``n`` is even, False if it is odd.
    """
    return n % 2 == 0


def square(n: float) -> float:
    """Return the square of a number.

    Args:
        n: The number to square.

    Returns:
        ``n`` multiplied by itself (``n * n``).
    """
    return n * n


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
    print(f"fibonacci(10) = {fibonacci(10)}")
