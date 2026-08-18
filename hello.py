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


def calculate_discount(subtotal: float, is_new_customer: bool) -> dict[str, float]:
    """Calculate discount, shipping, and total for an order.

    Discount rules:
    - Percentage discount applies at the highest qualifying tier only
      (20% at $200+, 10% at $100+, 0% below $100) and does not stack.
    - New customers get an additional flat $5 off, applied after the
      percentage discount.
    - Shipping is based on the undiscounted subtotal: free at $200+,
      free for new customers at $100+, otherwise $10.

    Args:
        subtotal: The order subtotal before discounts and shipping.
        is_new_customer: Whether the customer is new.

    Returns:
        A dict with subtotal, discount_rate, discount_amount,
        new_customer_discount, shipping, and total. Monetary values are
        rounded to two decimal places.
    """
    if subtotal >= 200:
        discount_rate = 0.20
    elif subtotal >= 100:
        discount_rate = 0.10
    else:
        discount_rate = 0.0

    discount_amount = round(subtotal * discount_rate, 2)
    new_customer_discount = 5.0 if is_new_customer else 0.0

    if subtotal >= 200 or (is_new_customer and subtotal >= 100):
        shipping = 0.0
    else:
        shipping = 10.0

    total = round(subtotal - discount_amount - new_customer_discount + shipping, 2)

    return {
        "subtotal": subtotal,
        "discount_rate": discount_rate,
        "discount_amount": discount_amount,
        "new_customer_discount": new_customer_discount,
        "shipping": shipping,
        "total": total,
    }


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
