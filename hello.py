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

__all__ = ["add", "calculate_discount", "fibonacci"]


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


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
    print(f"fibonacci(10) = {fibonacci(10)}")
