# FIXES

Summary
- Restored correct handling of negative numeric literals when `angle_mode` is enabled.
- Preserved the angle-mode feature (degrees ↔ radians) intact.

Root cause
- The tokenizer used a different, non-context-aware matching strategy in v1.1 when
  `angle_mode=True`. That change caused unary minus to be tokenized as a separate
  operator instead of part of the numeric literal.

What I changed
- Replaced the v1.1 tokenization branch with a single, context-aware tokenizer that
  properly recognizes unary minus (negative literals) regardless of `angle_mode`.
- No changes were required to `Calculator` logic that implements angle-mode behavior.

Why this fix
- Tokenization should be independent of the semantic `angle_mode` flag. The fix
  restores the original v1.0 behavior for numeric parsing while keeping the
  v1.1 trigonometric degree conversion.

Verification
- All tests (including regression tests) pass locally in the fixed directory.

How to run

```powershell
pip install -r requirements.txt
pytest tests/ -v
python src/calculator.py
```
