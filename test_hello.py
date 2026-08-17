"""Pytest tests for hello module."""
import pytest

from hello import add, multiply


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    # 浮点比较用 pytest.approx 避免 0.1 + 0.2 != 0.3 的精度问题
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_multiply_positive():
    assert multiply(2, 3) == 6


def test_multiply_negative():
    assert multiply(-2, 3) == -6


def test_multiply_zero():
    assert multiply(0, 5) == 0


def test_multiply_floats():
    assert multiply(0.1, 0.2) == pytest.approx(0.02)
