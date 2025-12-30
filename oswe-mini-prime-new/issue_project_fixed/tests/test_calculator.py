import pytest
from src.calculator import Calculator


def test_basic_arithmetic():
    calc = Calculator()
    assert calc.calculate("2 + 3 * 4") == 14.0


def test_parentheses():
    calc = Calculator()
    assert calc.calculate("(2 + 3) * 4") == 20.0


def test_functions_and_sqrt():
    calc = Calculator()
    assert calc.calculate("sqrt(16) + 2") == 6.0


def test_negative_literals_v1_0():
    calc = Calculator()
    calc.set_angle_mode(False)
    assert calc.calculate("-5 + 3") == -2.0


def test_angle_mode_positive():
    calc = Calculator()
    calc.set_angle_mode(True)
    assert calc.calculate("2 + 3") == 5.0
