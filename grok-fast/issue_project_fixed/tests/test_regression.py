"""
Regression Test Suite - Tests that NOW PASS in v1.1 when angle_mode=True
These tests verify the regression bug has been fixed.

BUG WAS:
When angle_mode was enabled (v1.1 feature), the tokenizer pattern was changed,
causing negative numbers to be incorrectly parsed. The pattern split "-5"
into two separate tokens: OPERATOR('-') and NUMBER('5'), instead of treating
it as a single NUMBER('-5') token.

FIX:
Modified tokenizer to use correct tokenization logic regardless of angle_mode,
since angle_mode only affects trigonometric function evaluation, not parsing.

VERIFIED SCENARIOS:
1. Negative literals: "-5 + 3" returns -2.0 ✓
2. Multiplication with negatives: "2 * (-3)" returns -6.0 ✓
3. Double negatives: "10 - -5" returns 15.0 ✓
"""

import pytest
from src.calculator import Calculator


class TestNegativeNumbersAngleMode:
    """
    Tests for negative number handling in v1.1 angle mode.
    
    These tests now PASS in v1.1 (angle_mode=True) after the fix.
    """
    
    def setup_method(self):
        """Set up calculator with angle mode enabled (v1.1)."""
        self.calc = Calculator()
        self.calc.set_angle_mode(True)  # Enable v1.1 angle mode
    
    def test_negative_plus_positive(self):
        """
        FIXED: Now correctly returns -2.0
        
        Working scenario (v1.1 fixed):
            "-5 + 3" = -2.0 ✓
        """
        result = self.calc.calculate("-5 + 3")
        assert result == -2.0, f"Expected -2.0, got {result}"
    
    def test_multiplication_with_negative(self):
        """
        FIXED: Now correctly returns -6.0
        
        Working scenario (v1.1 fixed):
            "2 * (-3)" = -6.0 ✓
        """
        result = self.calc.calculate("2 * (-3)")
        assert result == -6.0, f"Expected -6.0, got {result}"
    
    def test_double_negative(self):
        """
        FIXED: Now correctly returns 15.0
        
        Working scenario (v1.1 fixed):
            "10 - -5" = 15.0 ✓
        """
        result = self.calc.calculate("10 - -5")
        assert result == 15.0, f"Expected 15.0, got {result}"
    
    def test_negative_in_complex_expression(self):
        """
        FIXED: Now works correctly
        
        Working scenario (v1.1 fixed):
            "-5 + 3 * 2" = 1.0 ✓
        """
        result = self.calc.calculate("-5 + 3 * 2")
        assert result == 1.0, f"Expected 1.0, got {result}"
    
    def test_negative_literal(self):
        """
        FIXED: Negative literal works correctly
        
        Working scenario (v1.1 fixed):
            "-10" = -10.0 ✓
        """
        result = self.calc.calculate("-10")
        assert result == -10.0, f"Expected -10.0, got {result}"


class TestComparisonV1_0_vs_V1_1_Fixed:
    """
    Comparison tests showing v1.0 and v1.1 now both work correctly.
    """
    
    def test_comparison_negative_plus_positive(self):
        """Both v1.0 and v1.1 now return correct result."""
        # v1.0 behavior (stable)
        calc_v1_0 = Calculator()
        calc_v1_0.set_angle_mode(False)
        result_v1_0 = calc_v1_0.calculate("-5 + 3")
        
        # v1.1 behavior (fixed)
        calc_v1_1 = Calculator()
        calc_v1_1.set_angle_mode(True)
        result_v1_1 = calc_v1_1.calculate("-5 + 3")
        
        # Both should return -2.0
        assert result_v1_0 == -2.0, f"v1.0 should return -2.0, got {result_v1_0}"
        assert result_v1_1 == -2.0, f"v1.1 should return -2.0, got {result_v1_1}"
        assert result_v1_0 == result_v1_1, "v1.0 and v1.1 should return same result"
    
    def test_comparison_double_negative(self):
        """Both v1.0 and v1.1 now return correct result."""
        # v1.0 behavior (stable)
        calc_v1_0 = Calculator()
        calc_v1_0.set_angle_mode(False)
        result_v1_0 = calc_v1_0.calculate("10 - -5")
        
        # v1.1 behavior (fixed)
        calc_v1_1 = Calculator()
        calc_v1_1.set_angle_mode(True)
        result_v1_1 = calc_v1_1.calculate("10 - -5")
        
        # Both should return 15.0
        assert result_v1_0 == 15.0, f"v1.0 should return 15.0, got {result_v1_0}"
        assert result_v1_1 == 15.0, f"v1.1 should return 15.0, got {result_v1_1}"
        assert result_v1_0 == result_v1_1, "v1.0 and v1.1 should return same result"


class TestAngleModeStillWorks:
    """
    Tests showing that the angle mode feature still works correctly.
    """
    
    def test_angle_mode_feature_works(self):
        """Verify angle mode feature works correctly."""
        calc = Calculator()
        calc.set_angle_mode(True)
        
        # The new feature works fine
        result = calc.calculate("sin(30)")
        assert abs(result - 0.5) < 0.0001, "Angle mode feature works"
    
    def test_angle_mode_with_positive_numbers_works(self):
        """Verify angle mode works with positive numbers."""
        calc = Calculator()
        calc.set_angle_mode(True)
        
        # Basic math still works with positive numbers
        assert calc.calculate("2 + 3") == 5.0
        assert calc.calculate("2 * 3") == 6.0
        
        # Negative numbers now also work!
        assert calc.calculate("-5 + 3") == -2.0