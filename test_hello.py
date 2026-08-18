"""Pytest tests for the hello module."""

import pytest

from hello import add


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
