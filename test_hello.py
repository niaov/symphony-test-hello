"""Pytest tests for the hello module."""

from fractions import Fraction

import pytest

from hello import add, calculate_discount


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    # pytest.approx avoids binary float precision issues (0.1 + 0.2 != 0.3).
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_add_negative_floats():
    assert add(-0.5, -0.25) == pytest.approx(-0.75)


def test_add_mixed_int_and_float():
    assert add(1.5, 2) == pytest.approx(3.5)


def test_add_large_floats():
    assert add(1e15, 1e15) == pytest.approx(2e15)


def test_add_is_commutative():
    assert add(7, 8) == add(8, 7)


@pytest.mark.parametrize("value", ["a", None, [1, 2]])
def test_add_raises_type_error_for_non_numeric(value):
    with pytest.raises(TypeError):
        add(value, 1)


@pytest.mark.parametrize("value", [True, False])
def test_add_rejects_bool(value):
    with pytest.raises(TypeError, match="must be a real number"):
        add(value, 1)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_add_rejects_non_finite_floats(value):
    with pytest.raises(ValueError, match="must be finite"):
        add(value, 1)


def test_add_error_message_identifies_operand():
    with pytest.raises(TypeError, match="b must be a real number"):
        add(1, "oops")


def test_add_accepts_other_real_numbers():
    assert add(Fraction(1, 3), Fraction(1, 6)) == Fraction(1, 2)


@pytest.mark.parametrize(
    ("subtotal", "is_new_customer", "expected"),
    [
        # Returning customer, all three discount tiers.
        (50, False, {"discount_rate": 0.0, "discount_amount": 0.0,
                     "new_customer_discount": 0.0, "shipping": 10.0,
                     "total": 60.0}),
        (100, False, {"discount_rate": 0.10, "discount_amount": 10.0,
                      "new_customer_discount": 0.0, "shipping": 10.0,
                      "total": 100.0}),
        (200, False, {"discount_rate": 0.20, "discount_amount": 40.0,
                      "new_customer_discount": 0.0, "shipping": 0.0,
                      "total": 160.0}),
        # New customer, all three discount tiers.
        (50, True, {"discount_rate": 0.0, "discount_amount": 0.0,
                    "new_customer_discount": 5.0, "shipping": 10.0,
                    "total": 55.0}),
        (100, True, {"discount_rate": 0.10, "discount_amount": 10.0,
                     "new_customer_discount": 5.0, "shipping": 0.0,
                     "total": 85.0}),
        (200, True, {"discount_rate": 0.20, "discount_amount": 40.0,
                     "new_customer_discount": 5.0, "shipping": 0.0,
                     "total": 155.0}),
    ],
)
def test_calculate_discount_six_combinations(subtotal, is_new_customer, expected):
    result = calculate_discount(subtotal, is_new_customer)
    assert result["subtotal"] == subtotal
    for key, value in expected.items():
        assert result[key] == pytest.approx(value)


@pytest.mark.parametrize(
    ("subtotal", "is_new_customer", "rate", "shipping", "total"),
    [
        (99.99, False, 0.0, 10.0, 109.99),
        (100.0, False, 0.10, 10.0, 100.0),
        (150.0, False, 0.10, 10.0, 145.0),
        (199.99, False, 0.10, 10.0, 189.991),
        (200.0, False, 0.20, 0.0, 160.0),
        (99.99, True, 0.0, 10.0, 104.99),
        (100.0, True, 0.10, 0.0, 85.0),
        (150.0, True, 0.10, 0.0, 130.0),
        (199.99, True, 0.10, 0.0, 174.991),
        (200.0, True, 0.20, 0.0, 155.0),
    ],
)
def test_calculate_discount_boundaries(
    subtotal, is_new_customer, rate, shipping, total
):
    result = calculate_discount(subtotal, is_new_customer)
    assert result["discount_rate"] == pytest.approx(rate)
    assert result["discount_amount"] == pytest.approx(subtotal * rate)
    assert result["shipping"] == pytest.approx(shipping)
    assert result["total"] == pytest.approx(total)


def test_calculate_discount_new_customer_just_below_hundred():
    """Boundary: new customer just below $100 gets 0% tier and $5 off.

    Shipping is not free here: the new-customer free-shipping rule requires a
    subtotal of at least $100, so the flat $10 shipping applies.
    """
    result = calculate_discount(99.99, True)
    assert result["subtotal"] == pytest.approx(99.99)
    assert result["discount_rate"] == pytest.approx(0.0)
    assert result["discount_amount"] == pytest.approx(0.0)
    assert result["new_customer_discount"] == pytest.approx(5.0)
    assert result["shipping"] == pytest.approx(10.0)
    assert result["total"] == pytest.approx(104.99)


def test_calculate_discount_zero_subtotal():
    result = calculate_discount(0, False)
    assert result["discount_rate"] == 0.0
    assert result["discount_amount"] == pytest.approx(0.0)
    assert result["new_customer_discount"] == pytest.approx(0.0)
    assert result["shipping"] == pytest.approx(10.0)
    assert result["total"] == pytest.approx(10.0)


def test_calculate_discount_negative_subtotal():
    # Negative subtotals are accepted and evaluated deterministically.
    result = calculate_discount(-50, True)
    assert result["discount_rate"] == 0.0
    assert result["discount_amount"] == pytest.approx(0.0)
    assert result["new_customer_discount"] == pytest.approx(5.0)
    assert result["shipping"] == pytest.approx(10.0)
    assert result["total"] == pytest.approx(-45.0)


def test_calculate_discount_float_subtotal_in_tier():
    result = calculate_discount(123.45, False)
    assert result["discount_rate"] == pytest.approx(0.10)
    assert result["discount_amount"] == pytest.approx(12.345)
    assert result["shipping"] == pytest.approx(10.0)
    assert result["total"] == pytest.approx(121.105)


def test_calculate_discount_returns_expected_keys():
    result = calculate_discount(100, False)
    assert set(result) == {
        "subtotal",
        "discount_rate",
        "discount_amount",
        "new_customer_discount",
        "shipping",
        "total",
    }


@pytest.mark.parametrize("value", ["a", None, [1, 2]])
def test_calculate_discount_rejects_non_numeric_subtotal(value):
    with pytest.raises(TypeError):
        calculate_discount(value, False)


@pytest.mark.parametrize("value", [True, False])
def test_calculate_discount_rejects_bool_subtotal(value):
    with pytest.raises(TypeError, match="subtotal must be a real number"):
        calculate_discount(value, False)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_calculate_discount_rejects_non_finite_subtotal(value):
    with pytest.raises(ValueError, match="must be finite"):
        calculate_discount(value, False)


@pytest.mark.parametrize("value", [None, "yes", 1, 0, [True]])
def test_calculate_discount_rejects_non_bool_customer(value):
    with pytest.raises(TypeError, match="is_new_customer must be a bool"):
        calculate_discount(100, value)


def test_calculate_discount_accepts_other_real_numbers():
    result = calculate_discount(Fraction(100, 1), False)
    assert result["discount_rate"] == pytest.approx(0.10)
    assert result["discount_amount"] == pytest.approx(10.0)
