# Copied tests - unchanged (v1.0 stable + angle mode tests)

import pytest
import math
from src.calculator import Calculator


class TestBasicOperations:
    def setup_method(self):
        self.calc = Calculator()
        self.calc.set_angle_mode(False)

    def test_addition(self):
        assert self.calc.calculate("2 + 3") == 5.0
        assert self.calc.calculate("10 + 5") == 15.0

    def test_subtraction(self):
        assert self.calc.calculate("10 - 3") == 7.0
        assert self.calc.calculate("5 - 8") == -3.0

    def test_multiplication(self):
        assert self.calc.calculate("2 * 3") == 6.0
        assert self.calc.calculate("5 * 4") == 20.0

    def test_division(self):
        assert self.calc.calculate("10 / 2") == 5.0
        assert self.calc.calculate("15 / 3") == 5.0

    def test_power(self):
        assert self.calc.calculate("2 ^ 3") == 8.0
        assert self.calc.calculate("5 ^ 2") == 25.0

    def test_operator_precedence(self):
        assert self.calc.calculate("2 + 3 * 4") == 14.0
        assert self.calc.calculate("10 - 2 * 3") == 4.0

    def test_parentheses(self):
        assert self.calc.calculate("(2 + 3) * 4") == 20.0
        assert self.calc.calculate("(10 - 2) * 3") == 24.0


class TestNegativeNumbers:
    def setup_method(self):
        self.calc = Calculator()
        self.calc.set_angle_mode(False)

    def test_negative_literal(self):
        assert self.calc.calculate("-5") == -5.0
        assert self.calc.calculate("-10") == -10.0

    def test_negative_plus_positive(self):
        result = self.calc.calculate("-5 + 3")
        assert result == -2.0, f"Expected -2.0, got {result}"

    def test_multiplication_with_negative(self):
        result = self.calc.calculate("2 * (-3)")
        assert result == -6.0, f"Expected -6.0, got {result}"

    def test_subtraction_negative(self):
        result = self.calc.calculate("10 - -5")
        assert result == 15.0, f"Expected 15.0, got {result}"

    def test_negative_in_complex_expression(self):
        result = self.calc.calculate("-5 + 3 * 2")
        assert result == 1.0, f"Expected 1.0, got {result}"


class TestScientificFunctions:
    def setup_method(self):
        self.calc = Calculator()
        self.calc.set_angle_mode(False)

    def test_sqrt(self):
        assert self.calc.calculate("sqrt(16)") == 4.0
        assert self.calc.calculate("sqrt(25)") == 5.0

    def test_sqrt_with_arithmetic(self):
        assert self.calc.calculate("sqrt(16) + 2") == 6.0
        assert self.calc.calculate("sqrt(16) * 2") == 8.0

    def test_trigonometric_radian(self):
        result = self.calc.calculate("sin(0)")
        assert abs(result - 0.0) < 0.0001
        result = self.calc.calculate("cos(0)")
        assert abs(result - 1.0) < 0.0001

    def test_log(self):
        assert abs(self.calc.calculate("log(100)") - 2.0) < 0.0001
        assert abs(self.calc.calculate("ln(2.718281828)") - 1.0) < 0.0001


class TestAngleMode:
    def test_sin_degree_mode(self):
        calc = Calculator()
        calc.set_angle_mode(True)
        result = calc.calculate("sin(30)")
        assert abs(result - 0.5) < 0.0001, f"Expected 0.5, got {result}"
        result = calc.calculate("sin(90)")
        assert abs(result - 1.0) < 0.0001, f"Expected 1.0, got {result}"

    def test_cos_degree_mode(self):
        calc = Calculator()
        calc.set_angle_mode(True)
        result = calc.calculate("cos(60)")
        assert abs(result - 0.5) < 0.0001, f"Expected 0.5, got {result}"