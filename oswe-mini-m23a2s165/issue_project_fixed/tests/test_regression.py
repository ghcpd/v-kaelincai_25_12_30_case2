# Regression tests (copied unchanged) - should PASS after fix

import pytest
from src.calculator import Calculator


class TestRegressionNegativeNumbers:
    def setup_method(self):
        self.calc = Calculator()
        self.calc.set_angle_mode(True)

    def test_negative_plus_positive_regression(self):
        result = self.calc.calculate("-5 + 3")
        assert result == -2.0, f"Expected -2.0, got {result}"

    def test_multiplication_with_negative_regression(self):
        result = self.calc.calculate("2 * (-3)")
        assert result == -6.0, f"Expected -6.0, got {result}"

    def test_double_negative_regression(self):
        result = self.calc.calculate("10 - -5")
        assert result == 15.0, f"Expected 15.0, got {result}"

    def test_negative_in_complex_expression_regression(self):
        result = self.calc.calculate("-5 + 3 * 2")
        assert result == 1.0, f"Expected 1.0, got {result}"

    def test_negative_literal_regression(self):
        result = self.calc.calculate("-10")
        assert result == -10.0, f"Expected -10.0, got {result}"


class TestComparisonV1_0_vs_V1_1:
    def test_comparison_negative_plus_positive(self):
        calc_v1_0 = Calculator()
        calc_v1_0.set_angle_mode(False)
        result_v1_0 = calc_v1_0.calculate("-5 + 3")

        calc_v1_1 = Calculator()
        calc_v1_1.set_angle_mode(True)

        assert result_v1_0 == -2.0, f"v1.0 should return -2.0, got {result_v1_0}"
        result_v1_1 = calc_v1_1.calculate("-5 + 3")
        assert result_v1_1 == -2.0, f"v1.1 should return -2.0 after fix, got {result_v1_1}"

    def test_comparison_double_negative(self):
        calc_v1_0 = Calculator()
        calc_v1_0.set_angle_mode(False)
        result_v1_0 = calc_v1_0.calculate("10 - -5")

        calc_v1_1 = Calculator()
        calc_v1_1.set_angle_mode(True)

        assert result_v1_0 == 15.0, f"v1.0 should return 15.0, got {result_v1_0}"
        result_v1_1 = calc_v1_1.calculate("10 - -5")
        assert result_v1_1 == 15.0, f"v1.1 should return 15.0 after fix, got {result_v1_1}"


class TestAngleModeStillWorks:
    def test_angle_mode_feature_works(self):
        calc = Calculator()
        calc.set_angle_mode(True)
        result = calc.calculate("sin(30)")
        assert abs(result - 0.5) < 0.0001

    def test_angle_mode_with_positive_numbers_works(self):
        calc = Calculator()
        calc.set_angle_mode(True)
        assert calc.calculate("2 + 3") == 5.0
        assert calc.calculate("2 * 3") == 6.0