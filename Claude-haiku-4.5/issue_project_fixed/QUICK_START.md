# Scientific Calculator - Quick Start Guide

## Installation & Running

### One-Command Setup
```powershell
# Install dependencies and run tests
pip install -r requirements.txt ; pytest tests/ -v
```

## Project Overview

**Version:** 1.1 (with intentional regression bug)  
**Purpose:** Demonstration of regression bug in scientific calculator

### What Works (v1.0 - Radian Mode)
All functionality works correctly when angle_mode=False:
- ✅ Basic arithmetic
- ✅ Negative numbers  
- ✅ Parentheses
- ✅ Scientific functions
- ✅ Correct operator precedence

### What's Broken (v1.1 - Angle Mode)
When angle_mode=True, negative number parsing breaks:
- ❌ `-5 + 3` throws error (should be -2)
- ❌ `2 * (-3)` throws error (should be -6)
- ❌ `10 - -5` throws error (should be 15)
- ✅ Positive numbers still work fine
- ✅ Angle mode feature itself works (e.g., `sin(30)` = 0.5)

## Quick Demo

```powershell
# Run the demo script
python src/calculator.py
```

This shows side-by-side comparison of v1.0 (working) vs v1.1 (broken).

## Test Results

### All V1.0 Tests Pass (22 tests)
```powershell
pytest tests/test_calculator.py -v
```
All 18 tests pass when angle_mode=False.

### V1.1 Regression Tests Fail (5 tests)
```powershell
pytest tests/test_regression.py -v
```
5 tests **FAIL**, clearly demonstrating the bug.

### Full Test Suite
```powershell
pytest tests/ -v
```
**Expected Output:** 22 passed, **5 failed**

## Bug Details

**Root Cause:** Changes made to support the angle mode feature in v1.1 inadvertently disrupted the negative number handling that worked correctly in v1.0.

**Impact:** Negative numbers cause errors when angle mode is enabled, while all other functionality continues to work.

See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for detailed analysis.

## Project Structure
```
calculator_project/
├── src/
│   ├── calculator.py       # Main calculator logic
│   └── tokenizer.py        # Expression tokenization
├── tests/
│   ├── test_calculator.py  # V1.0 stable tests (all pass)
│   └── test_regression.py  # V1.1 bug tests (all fail)
├── README.md              # Full documentation
├── KNOWN_ISSUE.md         # Detailed bug analysis
├── QUICK_START.md         # This file
└── requirements.txt       # Dependencies
```

## Example Usage

```python
from src.calculator import Calculator

calc = Calculator()

# V1.0 Mode (works)
calc.set_angle_mode(False)
print(calc.calculate("-5 + 3"))    # -2.0 ✓
print(calc.calculate("2 * (-3)"))  # -6.0 ✓

# V1.1 Mode (broken)
calc.set_angle_mode(True)
print(calc.calculate("-5 + 3"))    # ERROR! ✗
print(calc.calculate("sin(30)"))   # 0.5 ✓ (new feature works)
```

## Key Takeaway

This project demonstrates a **classic regression bug**: adding a new feature (angle mode) broke previously working functionality (negative numbers). The negative number handling worked flawlessly for 8 months in v1.0, but the v1.1 refactoring inadvertently destroyed it.
