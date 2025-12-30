# Scientific Calculator Project

A command-line scientific calculator supporting basic arithmetic operations, parentheses, and scientific functions (sin, cos, sqrt, log, etc.).

## Project Status

**Current Version:** v1.1  
**Status:** ⚠️ KNOWN REGRESSION BUG

## Version History

- **v1.0** (Stable - 8 months production use)
  - Basic arithmetic operations: `+`, `-`, `*`, `/`, `^`
  - Parentheses support with correct precedence
  - Scientific functions: `sin`, `cos`, `tan`, `sqrt`, `log`, `ln`
  - Negative number support
  - **Status:** All features working correctly

- **v1.1** (Current - Regression introduced)
  - ✅ **New Feature:** Angle mode for trigonometric functions
  - ❌ **Regression:** Negative number parsing broken when angle mode is enabled

## Known Issue

⚠️ **CRITICAL REGRESSION BUG** - See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for details.

**Summary:** When angle mode is enabled, all expressions containing negative numbers fail or produce incorrect results. This represents a regression from v1.0 where all functionality worked correctly.

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

# Negative numbers (works in radian mode / v1.0)
calc.set_angle_mode(False)  # Radian mode - stable
result = calc.calculate("-5 + 3")  # Returns -2.0 ✓

# Negative numbers (BROKEN in angle mode / v1.1)
calc.set_angle_mode(True)  # Angle mode - buggy
result = calc.calculate("-5 + 3")  # ERROR! ✗ (should be -2.0)

# Angle mode feature (works correctly)
calc.set_angle_mode(True)
result = calc.calculate("sin(30)")  # Returns 0.5 (30 degrees)
```

### Demo Script

```powershell
python src/calculator.py
```

This will run a demo showing the difference between v1.0 behavior (radian mode) and v1.1 behavior (angle mode with bug).

## Known Issue Details

⚠️ **CRITICAL REGRESSION BUG** - See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for details.

**Summary:** When angle mode is enabled in v1.1, all expressions containing negative numbers fail. This functionality worked perfectly for 8 months in v1.0.

**Root Cause:** Changes made to support the angle mode feature inadvertently disrupted the expression parsing logic that handles negative numbers.

**Impact:** Engineers cannot use the calculator for any calculations involving negative values when angle mode is enabled.

## Running Tests

### Run all tests
```powershell
pytest tests/ -v
```

### Run only stable tests (v1.0 behavior)
```powershell
pytest tests/test_calculator.py -v
```

### Run regression tests (demonstrates the bug)
```powershell
pytest tests/test_regression.py -v
```

Expected output: **5 tests will FAIL**, demonstrating the regression bug introduced in v1.1.

### Run with coverage
```powershell
pytest tests/ --cov=src --cov-report=term-missing
```

## Project Structure

```
calculator_project/
├── src/
│   ├── __init__.py
│   ├── calculator.py       # Main calculator class
│   └── tokenizer.py        # Lexical analyzer
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py  # Tests for stable v1.0 behavior
│   └── test_regression.py  # Tests demonstrating the v1.1 bug
├── README.md               # This file
├── KNOWN_ISSUE.md         # Detailed bug documentation
└── requirements.txt        # Python dependencies
```

## Bug Reproduction

The regression bug can be reproduced with these simple test cases:

| Expression | v1.0 Result | v1.1 Result (Bug) | Status |
|------------|-------------|-------------------|--------|
| `-5 + 3` | `-2.0` ✓ | ERROR ✗ | FAIL |
| `2 * (-3)` | `-6.0` ✓ | ERROR ✗ | FAIL |
| `10 - -5` | `15.0` ✓ | ERROR ✗ | FAIL |
| `10 - -5` | `15.0` ✓ | `5.0` ✗ | FAIL |

See `tests/test_regression.py` for automated tests that demonstrate these failures.

## Contributing

This is a demonstration project showing a regression bug. The bug is intentionally left unfixed for educational purposes.

## License

MIT License - Educational demonstration project.
