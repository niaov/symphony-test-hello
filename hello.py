"""Minimal module for Symphony verification testing.

Contains basic arithmetic functions. Codex agent will be asked to extend this
(e.g. add a multiply function) via a GitHub issue, then create a PR.
"""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def calculate_discount(subtotal: float, is_new_customer: bool) -> dict[str, float | int]:
    """Calculate the final order total after discounts and shipping.

    Discounts:
    - Percentage: 20% off for subtotals >= $200, 10% off for subtotals >= $100,
      and 0% below $100 (only the highest applicable tier applies).
    - New customers get an additional flat $5 off, applied after the
      percentage discount.

    Shipping, decided after discounts: free for subtotals >= $200, or for
    new customers with subtotals >= $100; otherwise $10.

    Returns a dict with keys: subtotal, discount_rate, discount_amount,
    new_customer_discount, shipping, total.
    """
    if subtotal >= 200:
        discount_rate = 0.2
    elif subtotal >= 100:
        discount_rate = 0.1
    else:
        discount_rate = 0.0

    discount_amount = subtotal * discount_rate
    new_customer_discount = 5 if is_new_customer else 0

    if subtotal >= 200 or (is_new_customer and subtotal >= 100):
        shipping = 0
    else:
        shipping = 10

    total = subtotal - discount_amount - new_customer_discount + shipping
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
