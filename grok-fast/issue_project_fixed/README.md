# Scientific Calculator Project - FIXED

A command-line scientific calculator supporting basic arithmetic operations, parentheses, and scientific functions (sin, cos, sqrt, log, etc.).

## Project Status

**Current Version:** v1.1 (Fixed)  
**Status:** ✅ ALL TESTS PASSING

## Version History

- **v1.0** (Stable - 8 months production use)
  - Basic arithmetic operations: `+`, `-`, `*`, `/`, `^`
  - Parentheses support with correct precedence
  - Scientific functions: `sin`, `cos`, `tan`, `sqrt`, `log`, `ln`
  - Negative number support
  - **Status:** All features working correctly

- **v1.1** (Fixed - Regression resolved)
  - ✅ **New Feature:** Angle mode for trigonometric functions
  - ✅ **Fix:** Negative number parsing now works correctly in both modes

## Features

✅ **Basic arithmetic operations:** `+`, `-`, `*`, `/`, `^`  
✅ **Parentheses support** with correct precedence  
✅ **Scientific functions:** `sin`, `cos`, `tan`, `sqrt`, `log`, `ln`  
✅ **Negative number support** in all contexts  
✅ **Angle mode** for trigonometric functions (degrees vs radians)  

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```powershell
# Install dependencies
pip install -r requirements.txt
```

## Usage

### As a Module

```python
from src.calculator import Calculator

calc = Calculator()

# Basic calculations (works in both modes)
result = calc.calculate("2 + 3 * 4")  # Returns 14.0
result = calc.calculate("(2 + 3) * 4")  # Returns 20.0
result = calc.calculate("sqrt(16)")  # Returns 4.0

# Negative numbers (works in both radian and angle modes)
calc.set_angle_mode(False)  # Radian mode
result = calc.calculate("-5 + 3")  # Returns -2.0 ✓

calc.set_angle_mode(True)   # Angle mode
result = calc.calculate("-5 + 3")  # Returns -2.0 ✓ (FIXED!)

# Angle mode feature (works correctly)
calc.set_angle_mode(True)
result = calc.calculate("sin(30)")  # Returns 0.5 (30 degrees)
```

### Demo Script

```powershell
python src/calculator.py
```

This will run a demo showing the calculator works correctly in both radian mode and angle mode.

## Running Tests

### Run all tests
```powershell
pytest tests/ -v
```

### Expected Results
- **27 tests PASS** (0 failures)
- All v1.0 stable functionality preserved
- All v1.1 angle mode features working
- All negative number regression issues resolved

### Run with coverage
```powershell
pytest tests/ --cov=src --cov-report=term-missing
```

## Project Structure

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   ├── calculator.py       # Main calculator class
│   └── tokenizer.py        # Lexical analyzer (FIXED)
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py  # Tests for stable v1.0 behavior
│   └── test_regression.py  # Tests verifying v1.1 fixes
├── README.md               # This file
├── FIXES.md                # Documentation of the fix
└── requirements.txt        # Python dependencies
```

## Bug Fix Summary

The regression bug in v1.1 was caused by incorrect tokenization of negative numbers when angle mode was enabled. The fix ensures that:

1. **Tokenization is consistent** between angle mode and radian mode
2. **Negative numbers are parsed correctly** in all contexts
3. **Angle mode feature is preserved** for trigonometric functions
4. **All existing functionality continues to work**

See [FIXES.md](FIXES.md) for detailed information about the bug and fix.

## License

MIT License - Educational demonstration project.
