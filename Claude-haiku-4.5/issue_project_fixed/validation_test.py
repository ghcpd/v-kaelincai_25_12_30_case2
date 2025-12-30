"""
Comprehensive Validation Test Suite
Tests all functionality of the fixed scientific calculator
"""

from src.calculator import Calculator
import math

def print_header(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)

def print_section(text):
    print("\n[" + text + "]")
    print("-" * 70)

# Test 1: Angle mode feature verification
print_header("COMPREHENSIVE VALIDATION TEST SUITE")

print_section("TEST 1: Angle Mode Feature Verification (Degrees)")
calc = Calculator()

test_cases_angle = [
    ("sin(30)", 0.5, "sin(30°) should equal 0.5"),
    ("cos(60)", 0.5, "cos(60°) should equal 0.5"),
    ("sin(90)", 1.0, "sin(90°) should equal 1.0"),
    ("cos(90)", 0.0, "cos(90°) should equal 0.0"),
    ("cos(0)", 1.0, "cos(0°) should equal 1.0"),
]

calc.set_angle_mode(True)
print("Mode: Angle Mode ENABLED (Trigonometric functions use degrees)\n")

all_passed = True
for expr, expected, description in test_cases_angle:
    try:
        result = calc.calculate(expr)
        passed = abs(result - expected) < 1e-10
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {expr} = {result:.4f} (expected {expected})")
        print(f"       → {description}")
        if not passed:
            all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {expr} raised {type(e).__name__}: {e}")
        all_passed = False

# Test 2: Negative numbers with angle mode
print_section("TEST 2: Negative Number Handling with Angle Mode")
print("Mode: Angle Mode ENABLED (The primary regression fix test)\n")

test_cases_negative = [
    ("-5 + 3", -2.0, "Simple negative addition"),
    ("2 * (-3)", -6.0, "Multiplication with negative"),
    ("10 - -5", 15.0, "Double negative subtraction"),
    ("-5 * -2", 10.0, "Two negatives multiply"),
    ("(-10) / 2", -5.0, "Negative in parentheses"),
    ("-5 + 3 * 2", 1.0, "Negative with operator precedence"),
    ("-10", -10.0, "Negative literal"),
]

for expr, expected, description in test_cases_negative:
    try:
        result = calc.calculate(expr)
        passed = abs(result - expected) < 1e-10
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {expr:20} = {result:7.1f} (expected {expected:7.1f})")
        print(f"       → {description}")
        if not passed:
            all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {expr} raised {type(e).__name__}: {e}")
        all_passed = False

# Test 3: Radian mode verification
print_section("TEST 3: Radian Mode Verification (v1.0 Behavior)")
calc.set_angle_mode(False)
print("Mode: Angle Mode DISABLED (Trigonometric functions use radians)\n")

test_cases_radian = [
    ("sin(0)", 0.0, "sin(0 rad) = 0"),
    ("cos(0)", 1.0, "cos(0 rad) = 1"),
    ("-5 + 3", -2.0, "Negative numbers work in radian mode too"),
]

for expr, expected, description in test_cases_radian:
    try:
        result = calc.calculate(expr)
        passed = abs(result - expected) < 1e-10
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {expr:20} = {result:7.4f} (expected {expected:7.4f})")
        print(f"       → {description}")
        if not passed:
            all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {expr} raised {type(e).__name__}: {e}")
        all_passed = False

# Test 4: Basic operations still work
print_section("TEST 4: Basic Arithmetic Operations")
print("Mode: Angle Mode DISABLED (Standard v1.0 behavior)\n")

test_cases_basic = [
    ("2 + 3", 5.0, "Addition"),
    ("10 - 3", 7.0, "Subtraction"),
    ("2 * 3", 6.0, "Multiplication"),
    ("10 / 2", 5.0, "Division"),
    ("2 ^ 3", 8.0, "Exponentiation"),
    ("sqrt(16)", 4.0, "Square root"),
    ("2 + 3 * 4", 14.0, "Operator precedence"),
    ("(2 + 3) * 4", 20.0, "Parentheses"),
]

for expr, expected, description in test_cases_basic:
    try:
        result = calc.calculate(expr)
        passed = abs(result - expected) < 1e-10
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {expr:20} = {result:7.1f}")
        if not passed:
            all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {expr} raised {type(e).__name__}: {e}")
        all_passed = False

# Test 5: Complex expressions with negatives
print_section("TEST 5: Complex Expressions with Negative Numbers")
calc.set_angle_mode(True)
print("Mode: Angle Mode ENABLED (Complex expression validation)\n")

test_cases_complex = [
    ("sqrt(9) + (-2)", 1.0, "Square root with negative"),
    ("log(100) * (-1)", -2.0, "Log with negative multiplier"),
    ("2 * sqrt(4) - -3", 7.0, "Mixed operations with negative"),
]

for expr, expected, description in test_cases_complex:
    try:
        result = calc.calculate(expr)
        passed = abs(result - expected) < 1e-10
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {expr:30} = {result:7.1f} (expected {expected:7.1f})")
        if not passed:
            all_passed = False
    except Exception as e:
        print(f"✗ FAIL: {expr} raised {type(e).__name__}: {e}")
        all_passed = False

# Final summary
print_header("VALIDATION SUMMARY")
if all_passed:
    print("✓ ALL VALIDATION TESTS PASSED")
    print("\nThe fixed calculator successfully:")
    print("  ✓ Handles negative numbers in all contexts")
    print("  ✓ Supports angle mode for trigonometric functions")
    print("  ✓ Maintains all basic arithmetic operations")
    print("  ✓ Works correctly in both degree and radian modes")
    print("  ✓ Preserves operator precedence and parentheses")
else:
    print("✗ SOME TESTS FAILED - Review output above for details")

print("=" * 70 + "\n")
