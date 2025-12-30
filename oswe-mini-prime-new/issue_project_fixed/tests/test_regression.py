# Regression tests copied from original project

from src.calculator import Calculator


class TestRegressionNegativeNumbers:
    def setup_method(self):
        self.calc = Calculator()
        self.calc.set_angle_mode(True)

    def test_negative_plus_positive_regression(self):
        assert self.calc.calculate("-5 + 3") == -2.0

    def test_multiplication_with_negative_regression(self):
        assert self.calc.calculate("2 * (-3)") == -6.0

    def test_double_negative_regression(self):
        assert self.calc.calculate("10 - -5") == 15.0

    def test_negative_in_complex_expression_regression(self):
        assert self.calc.calculate("-5 + 3 * 2") == 1.0

    def test_negative_literal_regression(self):
        assert self.calc.calculate("-10") == -10.0


class TestAngleModeStillWorks:
    def test_angle_mode_feature_works(self):
        calc = Calculator()
        calc.set_angle_mode(True)
        assert abs(calc.calculate("sin(30)") - 0.5) < 0.0001

    def test_angle_mode_with_positive_numbers_works(self):
        calc = Calculator()
        calc.set_angle_mode(True)
        assert calc.calculate("2 + 3") == 5.0
        assert calc.calculate("2 * 3") == 6.0
