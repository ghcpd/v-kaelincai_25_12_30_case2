# Known Issue - Regression Bug in v1.1

## Issue Summary

**Issue Type:** Regression Bug  
**Severity:** Critical  
**Affected Version:** v1.1  
**Status:** Unresolved (Intentionally left for demonstration)

**Short Description:**  
Previously working scenario now fails. Negative number calculations broke after adding angle mode feature.

## Problem Description

### What Broke

When the angle mode feature was added in v1.1, all mathematical expressions containing negative numbers began failing or producing incorrect results. This functionality worked perfectly for 8 months in v1.0.

### Affected Scenarios

#### 1. Simple Negative Addition
- **Expression:** `-5 + 3`
- **Expected Result:** `-2.0`
- **Actual Result (v1.1):** `-8.0`
- **Impact:** Wrong calculation returned

#### 2. Multiplication with Negative in Parentheses
- **Expression:** `2 * (-3)`
- **Expected Result:** `-6.0`
- **Actual Result (v1.1):** `ValueError: Invalid expression`
- **Impact:** Application crashes

#### 3. Double Negative (Subtraction of Negative)
- **Expression:** `10 - -5`
- **Expected Result:** `15.0`
- **Actual Result (v1.1):** `5.0`
- **Impact:** Wrong calculation returned

#### 4. Negative in Complex Expressions
- **Expression:** `-5 + 3 * 2`
- **Expected Result:** `1.0`
- **Actual Result (v1.1):** Incorrect value
- **Impact:** Wrong calculation returned

## Technical Details

### Root Cause

When implementing the angle mode feature, the development team made changes to the expression parsing logic to accommodate the new functionality. This modification inadvertently broke the negative number recognition that had been working correctly for 8 months.

### Why This Causes Failures

The core issue lies in how mathematical expressions are broken down and interpreted by the calculator:

1. **Processing Change:** In v1.0, negative numbers like `-5` were correctly recognized as complete numeric values. In v1.1, the same input is now being split into separate components, causing the calculator to misinterpret the user's intent.

2. **Parser Confusion:** When the calculator encounters a negative number, it now tries to apply complex logic to determine whether the minus sign is part of the number or a separate operation. This logic fails in several common scenarios.

3. **Context Loss:** The system has lost the ability to use context clues to determine when a minus sign represents a negative number versus a subtraction operation. This affects:
   - Negative numbers at the start of expressions
   - Negative numbers in parentheses  
   - Double negatives (subtracting a negative number)

### Analysis

The bug appears to stem from changes made during the v1.1 implementation. While the new angle mode feature works correctly, the modifications to support it have disrupted the existing expression parsing pipeline in ways that specifically affect negative number handling.

## Trigger Conditions

### When the Bug Occurs
- Angle mode is enabled: `calculator.set_angle_mode(True)`
- Expression contains any negative number
- Can be negative literal, negative in parentheses, or double negative

### When the Bug Does NOT Occur
- Angle mode is disabled: `calculator.set_angle_mode(False)` (v1.0 behavior)
- Expression contains only positive numbers
- The angle mode feature itself (e.g., `sin(30)` in degrees) works correctly

## Impact Assessment

### User Impact
- **Severity:** Critical
- **Frequency:** Every expression with negative numbers
- **Users Affected:** All 500+ engineers using the calculator
- **Business Impact:** 
  - Engineering calculations produce wrong results
  - Some errors silent (wrong answer without warning)
  - Some errors loud (crashes with ValueError)
  - Lost productivity due to manual verification needed

### Test Results

When running the regression test suite (`tests/test_regression.py`):
- **5 tests FAIL** - All negative number tests fail in v1.1 angle mode
- All tests **PASS** in v1.0 mode (angle_mode=False)
- The failures clearly demonstrate the regression

## Reproduction Steps

### Automated (Recommended)
```powershell
pytest tests/test_regression.py -v
```

### Manual
```python
from src.calculator import Calculator

calc = Calculator()
calc.set_angle_mode(True)  # Enable v1.1 angle mode

# Bug manifests:
print(calc.calculate("-5 + 3"))     # Prints -8.0 (should be -2.0)
print(calc.calculate("2 * (-3)"))   # Raises ValueError (should be -6.0)
print(calc.calculate("10 - -5"))    # Prints 5.0 (should be 15.0)
```

## Investigation Notes

This regression demonstrates how seemingly unrelated changes can have unexpected consequences. The angle mode feature itself works perfectly - trigonometric functions correctly interpret degrees versus radians. However, the implementation approach chosen for this feature inadvertently disrupted the existing negative number handling.

### Lessons Learned

1. **Feature Isolation:** New features should be isolated to minimize impact on existing functionality
2. **Comprehensive Testing:** Test suites should cover edge cases that might be affected by unrelated changes
3. **Regression Testing:** Critical functionality (like negative numbers) should have dedicated regression tests
4. **Code Review:** Changes to core parsing logic require careful review for potential side effects

## Related Files

- `src/tokenizer.py` - Expression tokenization module
- `src/calculator.py` - Main calculator logic
- `tests/test_regression.py` - Automated tests demonstrating the bug
- `tests/test_calculator.py` - Tests showing v1.0 behavior still works

## References

- **Change Introduced:** v1.1 release (angle mode feature)
- **Previously Working Version:** v1.0 (8 months stable)
- **Related Feature:** Angle/Degree mode for trigonometric functions
- **Bug Category:** Regression (previously working scenario now fails)

---

**Note:** This bug is intentionally left unfixed for demonstration and educational purposes. This project serves as an example of how adding a new feature can inadvertently break existing functionality.
