"""Pytest tests for hello module."""
import pytest

from hello import add, subtract


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, 1) == 0


def test_add_zero():
    assert add(0, 0) == 0


def test_add_floats():
    # 浮点比较用 pytest.approx 避免 0.1 + 0.2 != 0.3 的精度问题
    assert add(0.1, 0.2) == pytest.approx(0.3)


def test_subtract_positive():
    assert subtract(5, 3) == 2


def test_subtract_negative():
    assert subtract(-5, -3) == -2


def test_subtract_zero():
    assert subtract(0, 5) == -5


def test_subtract_floats():
    assert subtract(0.3, 0.1) == pytest.approx(0.2)


def test_subtract_string_raises_type_error():
    with pytest.raises(TypeError, match="Expected number, got str"):
        subtract("5", 3)


def test_subtract_none_raises_type_error():
    with pytest.raises(TypeError, match="Expected number, got NoneType"):
        subtract(None, 3)


def test_subtract_bool_raises_type_error():
    with pytest.raises(TypeError, match="Expected number, got bool"):
        subtract(True, 3)
