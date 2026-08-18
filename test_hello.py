"""Pytest tests for hello module."""
import pytest

from hello import add, calculate_discount


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    # 浮点比较用 pytest.approx 避免 0.1 + 0.2 != 0.3 的精度问题
    assert add(0.1, 0.2) == pytest.approx(0.3)


@pytest.mark.parametrize(
    ("subtotal", "is_new_customer", "expected"),
    [
        # $150, existing customer -> 10% off, $10 shipping, total $145
        (
            150,
            False,
            {
                "discount_rate": 0.1,
                "discount_amount": pytest.approx(15),
                "new_customer_discount": 0,
                "shipping": 10,
                "total": pytest.approx(145),
            },
        ),
        # $250, existing customer -> 20% off, free shipping, total $200
        (
            250,
            False,
            {
                "discount_rate": 0.2,
                "discount_amount": pytest.approx(50),
                "new_customer_discount": 0,
                "shipping": 0,
                "total": pytest.approx(200),
            },
        ),
        # $80, new customer -> no %, $5 off, $10 shipping, total $85
        (
            80,
            True,
            {
                "discount_rate": 0.0,
                "discount_amount": 0,
                "new_customer_discount": 5,
                "shipping": 10,
                "total": pytest.approx(85),
            },
        ),
        # $120, new customer -> 10% off + $5 off, free shipping, total $103
        (
            120,
            True,
            {
                "discount_rate": 0.1,
                "discount_amount": pytest.approx(12),
                "new_customer_discount": 5,
                "shipping": 0,
                "total": pytest.approx(103),
            },
        ),
        # $200, new customer -> 20% off + $5 off, free shipping, total $155
        (
            200,
            True,
            {
                "discount_rate": 0.2,
                "discount_amount": pytest.approx(40),
                "new_customer_discount": 5,
                "shipping": 0,
                "total": pytest.approx(155),
            },
        ),
        # $50, existing customer -> no discount, $10 shipping, total $60
        (
            50,
            False,
            {
                "discount_rate": 0.0,
                "discount_amount": 0,
                "new_customer_discount": 0,
                "shipping": 10,
                "total": pytest.approx(60),
            },
        ),
    ],
)
def test_calculate_discount_cases(subtotal, is_new_customer, expected):
    result = calculate_discount(subtotal, is_new_customer)
    assert result["subtotal"] == subtotal
    assert result["discount_rate"] == expected["discount_rate"]
    assert result["discount_amount"] == expected["discount_amount"]
    assert result["new_customer_discount"] == expected["new_customer_discount"]
    assert result["shipping"] == expected["shipping"]
    assert result["total"] == expected["total"]


def test_calculate_discount_existing_100_boundary():
    # $100 is the lower percentage tier boundary: 10% off, $10 shipping.
    result = calculate_discount(100, False)
    assert result == {
        "subtotal": 100,
        "discount_rate": 0.1,
        "discount_amount": pytest.approx(10),
        "new_customer_discount": 0,
        "shipping": 10,
        "total": pytest.approx(100),
    }


def test_calculate_discount_existing_just_below_100():
    result = calculate_discount(99.99, False)
    assert result["discount_rate"] == 0.0
    assert result["discount_amount"] == 0
    assert result["shipping"] == 10
    assert result["total"] == pytest.approx(109.99)


def test_calculate_discount_existing_just_below_200():
    # Just below $200: 10% tier and $10 shipping still apply.
    result = calculate_discount(199.99, False)
    assert result["discount_rate"] == 0.1
    assert result["discount_amount"] == pytest.approx(19.999)
    assert result["shipping"] == 10
    assert result["total"] == pytest.approx(189.991)


def test_calculate_discount_existing_200_boundary():
    # $200 switches to the 20% tier and free shipping.
    result = calculate_discount(200, False)
    assert result["discount_rate"] == 0.2
    assert result["discount_amount"] == pytest.approx(40)
    assert result["shipping"] == 0
    assert result["total"] == pytest.approx(160)


def test_calculate_discount_new_customer_100_boundary():
    # New customers get free shipping from $100 onward.
    result = calculate_discount(100, True)
    assert result["discount_rate"] == 0.1
    assert result["new_customer_discount"] == 5
    assert result["shipping"] == 0
    assert result["total"] == pytest.approx(85)


def test_calculate_discount_new_customer_just_below_100():
    result = calculate_discount(99.99, True)
    assert result["discount_rate"] == 0.0
    assert result["new_customer_discount"] == 5
    assert result["shipping"] == 10
    assert result["total"] == pytest.approx(104.99)


def test_calculate_discount_zero_subtotal():
    result = calculate_discount(0, False)
    assert result["discount_rate"] == 0.0
    assert result["discount_amount"] == 0
    assert result["new_customer_discount"] == 0
    assert result["shipping"] == 10
    assert result["total"] == pytest.approx(10)
