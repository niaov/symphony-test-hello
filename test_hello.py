"""Pytest tests for the hello module."""

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


@pytest.mark.parametrize(
    ("subtotal", "is_new_customer", "expected"),
    [
        # Below $100: 0% off.
        (
            50.0,
            False,
            {
                "discount_rate": 0.0,
                "discount_amount": 0.0,
                "new_customer_discount": 0.0,
                "shipping": 10.0,
                "total": 60.0,
            },
        ),
        (
            50.0,
            True,
            {
                "discount_rate": 0.0,
                "discount_amount": 0.0,
                "new_customer_discount": 5.0,
                "shipping": 10.0,
                "total": 55.0,
            },
        ),
        # $100 <= subtotal < $200: 10% off, shipping free only for new customers.
        (
            150.0,
            False,
            {
                "discount_rate": 0.1,
                "discount_amount": 15.0,
                "new_customer_discount": 0.0,
                "shipping": 10.0,
                "total": 145.0,
            },
        ),
        (
            150.0,
            True,
            {
                "discount_rate": 0.1,
                "discount_amount": 15.0,
                "new_customer_discount": 5.0,
                "shipping": 0.0,
                "total": 130.0,
            },
        ),
        # subtotal >= $200: 20% off and free shipping for everyone.
        (
            250.0,
            False,
            {
                "discount_rate": 0.2,
                "discount_amount": 50.0,
                "new_customer_discount": 0.0,
                "shipping": 0.0,
                "total": 200.0,
            },
        ),
        (
            250.0,
            True,
            {
                "discount_rate": 0.2,
                "discount_amount": 50.0,
                "new_customer_discount": 5.0,
                "shipping": 0.0,
                "total": 195.0,
            },
        ),
    ],
)
def test_calculate_discount_tiers_and_customer_combinations(
    subtotal, is_new_customer, expected
):
    result = calculate_discount(subtotal, is_new_customer)
    assert result["subtotal"] == subtotal
    assert result["discount_rate"] == expected["discount_rate"]
    assert result["discount_amount"] == pytest.approx(expected["discount_amount"])
    assert result["new_customer_discount"] == pytest.approx(
        expected["new_customer_discount"]
    )
    assert result["shipping"] == pytest.approx(expected["shipping"])
    assert result["total"] == pytest.approx(expected["total"])


@pytest.mark.parametrize(
    ("subtotal", "is_new_customer", "expected"),
    [
        # $100: exactly at the 10% tier boundary.
        (
            100.0,
            False,
            {
                "discount_rate": 0.1,
                "discount_amount": 10.0,
                "new_customer_discount": 0.0,
                "shipping": 10.0,
                "total": 100.0,
            },
        ),
        (
            100.0,
            True,
            {
                "discount_rate": 0.1,
                "discount_amount": 10.0,
                "new_customer_discount": 5.0,
                "shipping": 0.0,
                "total": 85.0,
            },
        ),
        # $199.99: still 10%, not 20%.
        (
            199.99,
            False,
            {
                "discount_rate": 0.1,
                "discount_amount": 20.0,
                "new_customer_discount": 0.0,
                "shipping": 10.0,
                "total": 189.99,
            },
        ),
        (
            199.99,
            True,
            {
                "discount_rate": 0.1,
                "discount_amount": 20.0,
                "new_customer_discount": 5.0,
                "shipping": 0.0,
                "total": 174.99,
            },
        ),
        # $200: exactly at the 20% tier and free shipping boundary.
        (
            200.0,
            False,
            {
                "discount_rate": 0.2,
                "discount_amount": 40.0,
                "new_customer_discount": 0.0,
                "shipping": 0.0,
                "total": 160.0,
            },
        ),
        (
            200.0,
            True,
            {
                "discount_rate": 0.2,
                "discount_amount": 40.0,
                "new_customer_discount": 5.0,
                "shipping": 0.0,
                "total": 155.0,
            },
        ),
        # $0: lowest boundary.
        (
            0.0,
            False,
            {
                "discount_rate": 0.0,
                "discount_amount": 0.0,
                "new_customer_discount": 0.0,
                "shipping": 10.0,
                "total": 10.0,
            },
        ),
        (
            0.0,
            True,
            {
                "discount_rate": 0.0,
                "discount_amount": 0.0,
                "new_customer_discount": 5.0,
                "shipping": 10.0,
                "total": 5.0,
            },
        ),
    ],
)
def test_calculate_discount_boundary_values(subtotal, is_new_customer, expected):
    result = calculate_discount(subtotal, is_new_customer)
    assert result["subtotal"] == subtotal
    assert result["discount_rate"] == expected["discount_rate"]
    assert result["discount_amount"] == pytest.approx(expected["discount_amount"])
    assert result["new_customer_discount"] == pytest.approx(
        expected["new_customer_discount"]
    )
    assert result["shipping"] == pytest.approx(expected["shipping"])
    assert result["total"] == pytest.approx(expected["total"])


def test_calculate_discount_returns_expected_keys():
    result = calculate_discount(100.0, False)
    assert set(result) == {
        "subtotal",
        "discount_rate",
        "discount_amount",
        "new_customer_discount",
        "shipping",
        "total",
    }
