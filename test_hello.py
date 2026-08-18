"""Pytest tests for the hello module."""

from fractions import Fraction

import pytest

from hello import add, greet


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
    ("name", "expected"),
    [("Alice", "Hello, Alice!"), ("Bob", "Hello, Bob!")],
)
def test_greet_returns_expected_greeting(name, expected):
    assert greet(name) == expected


def test_greet_empty_name_raises_type_error():
    with pytest.raises(TypeError, match="name must be a non-empty string"):
        greet("")


@pytest.mark.parametrize("name", [123, None, ["Alice"]])
def test_greet_non_string_raises_type_error(name):
    with pytest.raises(TypeError, match="name must be a non-empty string"):
        greet(name)
