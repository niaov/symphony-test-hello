"""Pytest tests for hello module."""
import pytest

from hello import add
from hello import power


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    # 浮点比较用 pytest.approx 避免 0.1 + 0.2 != 0.3 的精度问题
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_power_zero_exponent():
    assert power(2, 0) == 1


def test_power_zero_to_zero():
    assert power(0, 0) == 1


def test_power_negative_exponent():
    assert power(2, -1) == pytest.approx(0.5)


def test_power_positive_exponent():
    assert power(2, 3) == 8
