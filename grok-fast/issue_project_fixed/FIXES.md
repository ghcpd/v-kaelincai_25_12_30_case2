# Bug Fix Documentation - Scientific Calculator Regression

## Issue Summary

**Bug:** Critical regression in v1.1 where negative number calculations failed when angle mode was enabled.

**Impact:** All expressions containing negative numbers produced incorrect results or crashed when angle mode was enabled.

**Root Cause:** The tokenizer was incorrectly modified to use different parsing logic for angle mode, breaking negative number recognition.

## What Was Broken

When `angle_mode=True`, these expressions failed:

| Expression | Expected | Actual (Buggy) |
|------------|----------|----------------|
| `-5 + 3` | `-2.0` | `-8.0` |
| `2 * (-3)` | `-6.0` | `ValueError` |
| `10 - -5` | `15.0` | `5.0` |

## Root Cause Analysis

### The Problem

In the original v1.0 code, the tokenizer used context-aware parsing that correctly identified negative numbers:

```python
# v1.0 logic (correct)
if ch.isdigit() or (ch == '-' and i + 1 < len(expression) and expression[i+1].isdigit() and
                    (i == 0 or expression[i-1] in '(+*/^-'))):
    # Parse as negative number
```

When v1.1 added angle mode, the tokenizer was mistakenly changed to use regex patterns that split negative numbers:

```python
# v1.1 buggy logic
self._pattern_v1_1 = r'(\d+\.?\d*)|([+\-*/^])|([()])|([a-z]+)'
# This splits "-5" into OPERATOR('-') and NUMBER('5')
```

### Why Angle Mode Affected Tokenization

The angle mode feature only needed to affect trigonometric function evaluation (converting degrees to radians), not expression parsing. However, the implementation incorrectly changed the tokenization logic based on the `angle_mode` flag.

## The Fix

### Changes Made

**File:** `src/tokenizer.py`

**Change:** Modified the `tokenize()` method to always use the correct tokenization logic:

```python
def tokenize(self, expression: str) -> List[Tuple[str, str]]:
    # FIX: Angle mode only affects trigonometric function evaluation, not tokenization
    # Use the correct tokenization logic regardless of angle_mode
    return self._tokenize_v1_0(expression)
```

### Why This Works

1. **Angle mode is irrelevant for parsing:** The `angle_mode` flag only affects how `sin`, `cos`, and `tan` functions are evaluated (degrees vs radians). It has no bearing on how arithmetic expressions are tokenized.

2. **Consistent tokenization:** Both modes now use the proven v1.0 tokenization logic that correctly handles negative numbers.

3. **Preserves angle mode feature:** Trigonometric functions still respect the angle mode setting during evaluation.

## Verification

### Test Results

After the fix, all tests pass:

```
pytest tests/ -v
======================== 27 passed, 0 failed ========================
```

### Specific Fixes Verified

| Expression | v1.0 | v1.1 (Before Fix) | v1.1 (After Fix) |
|------------|------|-------------------|------------------|
| `-5 + 3` | `-2.0` | `-8.0` ❌ | `-2.0` ✅ |
| `2 * (-3)` | `-6.0` | `ValueError` ❌ | `-6.0` ✅ |
| `10 - -5` | `15.0` | `5.0` ❌ | `15.0` ✅ |
| `sin(30)` in angle mode | N/A | `0.5` ✅ | `0.5` ✅ |

### Regression Prevention

The fix ensures that:
- ✅ All v1.0 functionality is preserved
- ✅ Angle mode feature continues to work
- ✅ Negative numbers work in both modes
- ✅ No existing working functionality is broken

## Files Changed

1. **`src/tokenizer.py`** - Fixed tokenization logic
2. **`tests/test_regression.py`** - Updated to reflect fixed behavior
3. **`README.md`** - Updated project status
4. **`FIXES.md`** - This documentation

## Lessons Learned

1. **Isolate feature changes:** New features should only affect the specific functionality they implement
2. **Test thoroughly:** Changes to core parsing logic require extensive testing
3. **Don't break working code:** Even seemingly unrelated changes can have unexpected consequences
4. **Consistent interfaces:** Tokenization should be consistent regardless of evaluation modes

## Testing the Fix

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