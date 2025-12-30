# Bug Fix Task - Scientific Calculator Regression

## Task Overview

You are a software engineer tasked with fixing a critical regression bug in a scientific calculator application. Your goal is to identify and fix the bug that was introduced in version 1.1, restoring the functionality that worked correctly in version 1.0.

## Current Situation

A scientific calculator has been in stable production for 8 months (v1.0). Recently, a new feature was added to support angle mode for trigonometric functions (v1.1). While the new feature works correctly, it has inadvertently broken the handling of negative numbers in mathematical expressions.

## Problem Description

**What's Broken:**
- All mathematical expressions containing negative numbers fail when angle mode is enabled
- Examples of failing expressions:
  - `-5 + 3` (should return -2.0)
  - `2 * (-3)` (should return -6.0)
  - `10 - -5` (should return 15.0)

**What Still Works:**
- All positive number calculations work fine
- The new angle mode feature itself works correctly (e.g., `sin(30)` in degrees)
- When angle mode is disabled (v1.0 behavior), everything works perfectly

## Your Task

1. **Analyze the codebase** to understand how the calculator works
2. **Identify the root cause** of the regression
3. **Implement a fix** that:
   - Restores negative number functionality in angle mode
   - Preserves the new angle mode feature
   - Does not break any existing working functionality
4. **Create a fixed version** in a new directory
5. **Verify the fix** by running all tests

## Requirements

### Directory Structure

Create the fixed version in a **new directory** with the following structure:

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   ├── calculator.py
│   └── tokenizer.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   └── test_regression.py
├── README.md
├── FIXES.md              # Document your changes here
└── requirements.txt
```

### Success Criteria

After your fix, running the test suite should show:
```
pytest tests/ -v
```
**Expected Result:** All 27 tests PASS (0 failures)

This includes:
- ✅ All 18 v1.0 stable tests must still pass
- ✅ All 5 regression tests must now pass (currently failing)
- ✅ All 4 other tests must still pass

### Constraints

1. **Do NOT modify the original project** in `issue_project/`
2. **Create all files in the new directory** `issue_project_fixed/`
3. **Preserve all working functionality** - do not break what currently works
4. **Maintain the angle mode feature** - it should continue to work
5. **Fix must work on both modes** - angle mode ON and OFF

## Investigation Starting Points

1. **Review the test failures** to understand what's expected:
   ```
   pytest tests/test_regression.py -v
   ```

2. **Compare behavior** between angle mode enabled vs disabled:
   ```
   python src/calculator.py
   ```

3. **Examine the code** to understand the flow:
   - How are expressions tokenized?
   - How does angle mode affect parsing?
   - What changed between v1.0 and v1.1?

## Deliverables

1. **Fixed codebase** in `issue_project_fixed/` directory
2. **FIXES.md** document containing:
   - Description of what you found
   - What you changed and why
   - How you verified the fix
3. **All tests passing** when run from the new directory

## Notes

- The bug is related to how mathematical expressions are parsed
- The issue only manifests when angle mode is enabled
- The original v1.0 behavior (angle mode disabled) still works correctly
- Focus on understanding the difference between how v1.0 and v1.1 process input

## Testing Your Fix

From the `issue_project_fixed/` directory:

```powershell
# Install dependencies
pip install -r requirements.txt

# Run all tests - should see 27 passed, 0 failed
pytest tests/ -v

# Run demo - should show no errors in either mode
python src/calculator.py

# Specifically test the regression cases
pytest tests/test_regression.py -v
```

All tests must pass for the fix to be considered complete.

---

**Remember:** Your goal is to restore the negative number functionality without breaking the new angle mode feature or any other working functionality. Good luck!
