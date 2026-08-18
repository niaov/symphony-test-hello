"""Pytest tests for hello module."""

import pytest

from hello import add, multiply, subtract


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 5),
        (-1, 1, 0),
        (0, 0, 0),
        (0.1, 0.2, 0.3),
    ],
)
def test_add(a, b, expected):
    assert add(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (5, 3, 2),
        (-5, -3, -2),
        (0, 5, -5),
        (0.3, 0.1, 0.2),
    ],
)
def test_subtract(a, b, expected):
    assert subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 6),
        (-2, 3, -6),
        (0, 5, 0),
        (0.1, 0.2, 0.02),
    ],
)
def test_multiply(a, b, expected):
    assert multiply(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("func", [add, subtract, multiply])
@pytest.mark.parametrize("bad_value", ["5", None, True, [1]])
def test_operations_reject_non_numeric_input(func, bad_value):
    with pytest.raises(TypeError, match=r"Expected number for a, got \w+"):
        func(bad_value, 3)


@pytest.mark.parametrize("func", [add, subtract, multiply])
@pytest.mark.parametrize("bad_value", ["5", None, False, {"a": 1}])
def test_operations_reject_non_numeric_second_argument(func, bad_value):
    with pytest.raises(TypeError, match=r"Expected number for b, got \w+"):
        func(3, bad_value)


@pytest.mark.parametrize("func", [add, subtract, multiply])
def test_operations_accept_ints_and_floats(func):
    assert func(3, 2) == func(3.0, 2)
