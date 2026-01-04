"""
Basic test suite for calculator functionality.
Tests the stable v1.0 behavior (radian mode / angle_mode=False).
"""

import pytest
import math
from src.calculator import Calculator


class TestBasicOperations:
    """Test basic arithmetic operations."""
    
    def setup_method(self):
        """Set up test calculator instance."""
        self.calc = Calculator()
        self.calc.set_angle_mode(False)  # Use v1.0 stable behavior
    
    def test_addition(self):
        """Test simple addition."""
        assert self.calc.calculate("2 + 3") == 5.0
        assert self.calc.calculate("10 + 5") == 15.0
    
    def test_subtraction(self):
        """Test simple subtraction."""
        assert self.calc.calculate("10 - 3") == 7.0
        assert self.calc.calculate("5 - 8") == -3.0
    
    def test_multiplication(self):
        """Test simple multiplication."""
        assert self.calc.calculate("2 * 3") == 6.0
        assert self.calc.calculate("5 * 4") == 20.0
    
    def test_division(self):
        """Test simple division."""
        assert self.calc.calculate("10 / 2") == 5.0
        assert self.calc.calculate("15 / 3") == 5.0
    
    def test_power(self):
        """Test exponentiation."""
        assert self.calc.calculate("2 ^ 3") == 8.0
        assert self.calc.calculate("5 ^ 2") == 25.0
    
    def test_operator_precedence(self):
        """Test correct operator precedence."""
        assert self.calc.calculate("2 + 3 * 4") == 14.0
        assert self.calc.calculate("10 - 2 * 3") == 4.0
    
    def test_parentheses(self):
        """Test parentheses override precedence."""
        assert self.calc.calculate("(2 + 3) * 4") == 20.0
        assert self.calc.calculate("(10 - 2) * 3") == 24.0


class TestNegativeNumbers:
    """Test negative number handling - STABLE in v1.0."""
    
    def setup_method(self):
        """Set up test calculator instance."""
        self.calc = Calculator()
        self.calc.set_angle_mode(False)  # Use v1.0 stable behavior
    
    def test_negative_literal(self):
        """Test negative number as literal."""
        assert self.calc.calculate("-5") == -5.0
        assert self.calc.calculate("-10") == -10.0
    
    def test_negative_plus_positive(self):
        """Test negative number plus positive number."""
        result = self.calc.calculate("-5 + 3")
        assert result == -2.0, f"Expected -2.0, got {result}"
    
    def test_multiplication_with_negative(self):
        """Test multiplication with negative number in parentheses."""
        result = self.calc.calculate("2 * (-3)")
        assert result == -6.0, f"Expected -6.0, got {result}"
    
    def test_subtraction_negative(self):
        """Test subtracting a negative (double negative)."""
        result = self.calc.calculate("10 - -5")
        assert result == 15.0, f"Expected 15.0, got {result}"
    
    def test_negative_in_complex_expression(self):
        """Test negative numbers in complex expressions."""
        result = self.calc.calculate("-5 + 3 * 2")
        assert result == 1.0, f"Expected 1.0, got {result}"


class TestScientificFunctions:
    """Test scientific functions."""
    
    def setup_method(self):
        """Set up test calculator instance."""
        self.calc = Calculator()
        self.calc.set_angle_mode(False)  # Radian mode
    
    def test_sqrt(self):
        """Test square root function."""
        assert self.calc.calculate("sqrt(16)") == 4.0
        assert self.calc.calculate("sqrt(25)") == 5.0
    
    def test_sqrt_with_arithmetic(self):
        """Test sqrt in arithmetic expressions."""
        assert self.calc.calculate("sqrt(16) + 2") == 6.0
        assert self.calc.calculate("sqrt(16) * 2") == 8.0
    
    def test_trigonometric_radian(self):
        """Test trigonometric functions in radian mode."""
        # sin(0) = 0
        result = self.calc.calculate("sin(0)")
        assert abs(result - 0.0) < 0.0001
        
        # cos(0) = 1
        result = self.calc.calculate("cos(0)")
        assert abs(result - 1.0) < 0.0001
    
    def test_log(self):
        """Test logarithm functions."""
        assert abs(self.calc.calculate("log(100)") - 2.0) < 0.0001
        assert abs(self.calc.calculate("ln(2.718281828)") - 1.0) < 0.0001


class TestAngleMode:
    """Test angle mode feature (v1.1)."""
    
    def test_sin_degree_mode(self):
        """Test sine function in degree mode."""
        calc = Calculator()
        calc.set_angle_mode(True)
        
        # sin(30°) = 0.5
        result = calc.calculate("sin(30)")
        assert abs(result - 0.5) < 0.0001, f"Expected 0.5, got {result}"
        
        # sin(90°) = 1.0
        result = calc.calculate("sin(90)")
        assert abs(result - 1.0) < 0.0001, f"Expected 1.0, got {result}"
    
    def test_cos_degree_mode(self):
        """Test cosine function in degree mode."""
        calc = Calculator()
        calc.set_angle_mode(True)
        
        # cos(60°) = 0.5
        result = calc.calculate("cos(60)")
        assert abs(result - 0.5) < 0.0001, f"Expected 0.5, got {result}"
