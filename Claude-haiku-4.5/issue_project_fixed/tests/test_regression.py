"""
Regression Test Suite - Tests that FAIL in v1.1 when angle_mode=True
These tests demonstrate the regression bug introduced in v1.1.

BUG DESCRIPTION:
When angle_mode is enabled (v1.1 feature), the tokenizer pattern was changed,
causing negative numbers to be incorrectly parsed. The pattern now splits "-5"
into two separate tokens: OPERATOR('-') and NUMBER('5'), instead of treating
it as a single NUMBER('-5') token.

IMPACT:
- All expressions with negative numbers fail or produce incorrect results
- This breaks functionality that worked perfectly for 8 months in v1.0

AFFECTED SCENARIOS:
1. Negative literals: "-5 + 3" returns -8 instead of -2
2. Multiplication with negatives: "2 * (-3)" raises syntax error
3. Double negatives: "10 - -5" returns 5 instead of 15
"""

import pytest
from src.calculator import Calculator


class TestRegressionNegativeNumbers:
    """
    Regression tests for negative number handling in v1.1 angle mode.
    
    These tests PASS in v1.0 (angle_mode=False) but FAIL in v1.1 (angle_mode=True).
    All tests in this class will FAIL when run, demonstrating the regression bug.
    """
    
    def setup_method(self):
        """Set up calculator with angle mode enabled (v1.1)."""
        self.calc = Calculator()
        self.calc.set_angle_mode(True)  # Enable v1.1 angle mode - triggers bug
    
    def test_negative_plus_positive_regression(self):
        """
        BUG: Raises error instead of returning -2.0
        
        Previously working scenario (v1.0):
            "-5 + 3" = -2.0 ✓
        
        Current behavior (v1.1 with angle_mode):
            "-5 + 3" = -8.0 ✗
        
        Root cause:
            Tokenizer splits "-5" into ['-', '5']
            Parser interprets this as unary minus of (5 + 3) = -(8) = -8
        
        Location: src/tokenizer.py, line 33 (_pattern_v1_1)
        """
        result = self.calc.calculate("-5 + 3")
        assert result == -2.0, f"Expected -2.0, got {result}"
    
    def test_multiplication_with_negative_regression(self):
        """
        BUG: Raises ValueError instead of returning -6.0
        
        Previously working scenario (v1.0):
            "2 * (-3)" = -6.0 ✓
        
        Current behavior (v1.1 with angle_mode):
            "2 * (-3)" raises ValueError ✗
        
        Root cause:
            Tokenizer splits "(-3)" into ['(', '-', '3', ')']
            Parser sees OPERATOR('-') after LPAREN
            Tries to handle unary minus but fails with parentheses
        
        Location: src/tokenizer.py, line 33 (_pattern_v1_1)
        """
        result = self.calc.calculate("2 * (-3)")
        assert result == -6.0, f"Expected -6.0, got {result}"
    
    def test_double_negative_regression(self):
        """
        BUG: Raises error instead of returning 15.0
        
        Previously working scenario (v1.0):
            "10 - -5" = 15.0 ✓
        
        Current behavior (v1.1 with angle_mode):
            "10 - -5" = 5.0 ✗
        
        Root cause:
            Tokenizer splits "--5" into ['-', '-', '5']
            Parser misinterprets the double negative
            Results in 10 - 5 = 5 instead of 10 + 5 = 15
        
        Location: src/tokenizer.py, line 33 (_pattern_v1_1)
        """
        result = self.calc.calculate("10 - -5")
        assert result == 15.0, f"Expected 15.0, got {result}"
    
    def test_negative_in_complex_expression_regression(self):
        """
        BUG: Raises error
        
        Previously working scenario (v1.0):
            "-5 + 3 * 2" = 1.0 ✓
        
        Current behavior (v1.1 with angle_mode):
            "-5 + 3 * 2" = incorrect result ✗
        
        Root cause:
            Same tokenizer issue affects complex expressions
        
        Location: src/tokenizer.py, line 33 (_pattern_v1_1)
        """
        result = self.calc.calculate("-5 + 3 * 2")
        assert result == 1.0, f"Expected 1.0, got {result}"
    
    def test_negative_literal_regression(self):
        """
        BUG: Negative literal parsed incorrectly
        
        Previously working scenario (v1.0):
            "-10" = -10.0 ✓
        
        Current behavior (v1.1 with angle_mode):
            "-10" may fail or return incorrect value ✗
        
        Root cause:
            Tokenizer cannot properly handle standalone negative numbers
        
        Location: src/tokenizer.py, line 33 (_pattern_v1_1)
        """
        result = self.calc.calculate("-10")
        assert result == -10.0, f"Expected -10.0, got {result}"


class TestComparisonV1_0_vs_V1_1:
    """
    Side-by-side comparison tests showing v1.0 and v1.1 both work after fix.
    These tests verify that the regression has been fixed.
    """
    
    def test_comparison_negative_plus_positive(self):
        """Direct comparison: v1.0 and v1.1 both work correctly after fix."""
        # v1.0 behavior (stable)
        calc_v1_0 = Calculator()
        calc_v1_0.set_angle_mode(False)
        result_v1_0 = calc_v1_0.calculate("-5 + 3")
        
        # v1.1 behavior (fixed)
        calc_v1_1 = Calculator()
        calc_v1_1.set_angle_mode(True)
        
        # Assert both return the correct value
        assert result_v1_0 == -2.0, f"v1.0 should return -2.0, got {result_v1_0}"
        result_v1_1 = calc_v1_1.calculate("-5 + 3")
        assert result_v1_1 == -2.0, (
            f"FIXED: v1.1 now correctly returns {result_v1_1} = -2.0. "
            f"The regression has been fixed!"
        )
    
    def test_comparison_double_negative(self):
        """Direct comparison: v1.0 and v1.1 both work correctly after fix."""
        # v1.0 behavior (stable)
        calc_v1_0 = Calculator()
        calc_v1_0.set_angle_mode(False)
        result_v1_0 = calc_v1_0.calculate("10 - -5")
        
        # v1.1 behavior (fixed)
        calc_v1_1 = Calculator()
        calc_v1_1.set_angle_mode(True)
        
        # Assert both return the correct value
        assert result_v1_0 == 15.0, f"v1.0 should return 15.0, got {result_v1_0}"
        result_v1_1 = calc_v1_1.calculate("10 - -5")
        assert result_v1_1 == 15.0, (
            f"FIXED: v1.1 now correctly returns {result_v1_1} = 15.0. "
            f"The regression has been fixed!"
        )


class TestAngleModeStillWorks:
    """
    Tests showing that the angle mode feature itself works.
    The bug only affects negative number parsing, not angle calculations.
    """
    
    def test_angle_mode_feature_works(self):
        """Verify angle mode feature (the new v1.1 feature) works correctly."""
        calc = Calculator()
        calc.set_angle_mode(True)
        
        # The new feature works fine
        result = calc.calculate("sin(30)")
        assert abs(result - 0.5) < 0.0001, "Angle mode feature itself works"
    
    def test_angle_mode_with_positive_numbers_works(self):
        """Verify angle mode works with positive numbers."""
        calc = Calculator()
        calc.set_angle_mode(True)
        
        # Basic math still works with positive numbers
        assert calc.calculate("2 + 3") == 5.0
        assert calc.calculate("2 * 3") == 6.0
        
        # The bug ONLY affects negative numbers!
