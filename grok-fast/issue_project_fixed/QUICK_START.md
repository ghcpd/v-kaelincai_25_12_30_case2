# Scientific Calculator - Quick Start Guide (FIXED)

## Installation & Running

### One-Command Setup
```powershell
# Install dependencies and run tests
pip install -r requirements.txt ; pytest tests/ -v
```

## Project Overview

**Version:** 1.1 (Fixed)  
**Status:** ✅ All 27 tests passing  
**Purpose:** Scientific calculator with angle mode and negative number support

### What Works (Both Modes)
All functionality works correctly in both radian mode and angle mode:
- ✅ Basic arithmetic
- ✅ Negative numbers in all contexts
- ✅ Parentheses
- ✅ Scientific functions
- ✅ Correct operator precedence
- ✅ Angle mode for trigonometric functions

### Fixed Issues
Previously broken expressions now work correctly:
- ✅ `-5 + 3` = -2.0
- ✅ `2 * (-3)` = -6.0
- ✅ `10 - -5` = 15.0
- ✅ All negative number scenarios

## Quick Demo

```powershell
# Run the demo script
python src/calculator.py
```

This shows the calculator working correctly in both radian mode and angle mode.

## Test Results

### All Tests Pass (27 tests)
```powershell
pytest tests/ -v
```

**Result:** 27 passed, 0 failed

### Test Breakdown
- **18 stable tests** (v1.0 functionality) ✅
- **5 regression tests** (negative numbers in angle mode) ✅
- **4 angle mode tests** (trigonometric functions) ✅

## Usage Examples

### Basic Calculations
```python
from src.calculator import Calculator

calc = Calculator()

# Works in both modes
calc.calculate("2 + 3 * 4")        # 14.0
calc.calculate("(2 + 3) * 4")      # 20.0
calc.calculate("sqrt(16) + 2")     # 6.0
```

### Negative Numbers (Now Fixed)
```python
calc = Calculator()

# Radian mode
calc.set_angle_mode(False)
calc.calculate("-5 + 3")           # -2.0
calc.calculate("2 * (-3)")         # -6.0
calc.calculate("10 - -5")          # 15.0

# Angle mode (previously broken, now fixed)
calc.set_angle_mode(True)
calc.calculate("-5 + 3")           # -2.0 ✅
calc.calculate("2 * (-3)")         # -6.0 ✅
calc.calculate("10 - -5")          # 15.0 ✅
```

### Angle Mode Features
```python
calc = Calculator()
calc.set_angle_mode(True)

calc.calculate("sin(30)")          # 0.5 (30 degrees)
calc.calculate("cos(60)")          # 0.5 (60 degrees)
calc.calculate("sin(30) + (-5)")   # -4.5 (angle mode + negative)
```

## Key Fix

**Problem:** Angle mode broke negative number parsing due to incorrect tokenizer changes.

**Solution:** Modified tokenizer to use consistent parsing logic regardless of angle mode, since angle mode only affects trigonometric function evaluation.

**Result:** All functionality works in both modes, preserving the angle mode feature while fixing the regression.

## Files Changed

- `src/tokenizer.py` - Fixed tokenization logic
- `tests/test_regression.py` - Updated test expectations
- `README.md` - Updated status
- `FIXES.md` - Added fix documentation

See [FIXES.md](FIXES.md) for detailed technical information.