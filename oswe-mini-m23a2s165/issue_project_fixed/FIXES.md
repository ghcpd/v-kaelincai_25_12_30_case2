# FIXES.md

## Summary

Fixed a regression introduced in v1.1 where negative numbers were parsed
incorrectly when `angle_mode` was enabled. The bug was in `tokenizer.py`:
when angle mode was enabled the tokenizer used a regex-only approach that
split leading '-' from numeric literals.

## What I changed

- Replaced the regex-only tokenization for angle mode with a context-aware
  tokenizer that correctly recognizes negative literals (`-5`, `(-3)`,
  `10 - -5`) while preserving the `angle_mode` behavior for trigonometric
  functions.
- All other logic (calculator evaluation, shunting-yard, function handling)
  remains unchanged.

Files added/modified in `issue_project_fixed/`:
- `src/tokenizer.py` — fixed tokenizer (context-aware parsing for negatives)
- `src/calculator.py` — copied from original (uses fixed tokenizer)
- `tests/*` — copied tests; regression tests now pass
- `FIXES.md`, `README.md`, `requirements.txt`

## Why this fixes the problem

The original v1.1 change swapped the tokenizer to a regex-driven pattern
that does not consider the parsing context for a '-' character. By using
the same context-aware logic used in v1.0 for negative-number detection
we restore the correct behavior without changing the angle-mode feature.

## Verification

From `issue_project_fixed/`:

```powershell
pip install -r requirements.txt
pytest tests/ -v
python src/calculator.py
```

All tests pass and demo expressions (including negative-number cases and
trigonometric degree-mode calculations) work as expected.
