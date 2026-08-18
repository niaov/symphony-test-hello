"""Pytest tests for hello module."""
import pytest

from hello import add, divide


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    # 浮点比较用 pytest.approx 避免 0.1 + 0.2 != 0.3 的精度问题
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_divide_positive():
    assert divide(6, 3) == 2


def test_divide_negative():
    assert divide(-6, 3) == -2


def test_divide_zero():
    assert divide(0, 5) == 0


def test_divide_floats():
    assert divide(1.0, 4.0) == pytest.approx(0.25)


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(1, 0)
