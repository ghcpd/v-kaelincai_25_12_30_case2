"""
Tokenizer module for mathematical expressions (fixed version).

Fix applied: ensure negative numbers are recognized when angle_mode is enabled.
The original v1.1 mistakenly used a regex-only tokenizer that split leading
negative signs into separate operator tokens. Fixed by using the same
context-aware tokenization logic for both modes (preserves angle mode feature
while restoring correct negative-number handling).
"""

import re
from typing import List, Tuple


class Tokenizer:
    """Tokenizes mathematical expressions into processable tokens."""

    # Token types
    NUMBER = 'NUMBER'
    OPERATOR = 'OPERATOR'
    FUNCTION = 'FUNCTION'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

    def __init__(self, angle_mode: bool = False):
        """
        Initialize tokenizer.

        Args:
            angle_mode: If True, use angle mode for trigonometric functions
        """
        self.angle_mode = angle_mode

        # Keep regex patterns for compatibility / future use but do NOT rely on
        # the regex-only tokenizer for parsing negative numbers.
        self._pattern_v1_0 = r'(-?\d+\.?\d*)|([+*/^])|([()])|([a-z]+)'
        self._pattern_v1_1 = r'(\d+\.?\d*)|([+\-*/^])|([()])|([a-z]+)'

        # Always prefer the context-aware tokenizer which correctly handles
        # negative numbers. This preserves the angle_mode feature while fixing
        # the regression introduced in v1.1.
        self.pattern = self._pattern_v1_0

    def tokenize(self, expression: str) -> List[Tuple[str, str]]:
        """
        Tokenize a mathematical expression.
        """
        expression = expression.replace(' ', '')  # Remove whitespace

        # Use context-aware tokenization for both modes (fixes regression)
        return self._tokenize_context_aware(expression)

    def _tokenize_context_aware(self, expression: str) -> List[Tuple[str, str]]:
        """Context-aware tokenization that correctly treats leading '-' as
        part of a number when appropriate (handles cases like -5, 2*(-3),
        and 10 - -5).
        """
        tokens = []
        i = 0

        while i < len(expression):
            ch = expression[i]

            # Number (including negative when '-' appears in number context)
            if ch.isdigit() or (
                ch == '-' and i + 1 < len(expression) and expression[i + 1].isdigit() and
                (i == 0 or expression[i - 1] in '(+*/^-')
            ):
                num_str = ''
                if ch == '-':
                    num_str = '-'
                    i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append((self.NUMBER, num_str))
                continue

            # Operators
            if ch in '+-*/^':
                tokens.append((self.OPERATOR, ch))
                i += 1
                continue

            # Parentheses
            if ch == '(':
                tokens.append((self.LPAREN, ch))
                i += 1
                continue
            if ch == ')':
                tokens.append((self.RPAREN, ch))
                i += 1
                continue

            # Function names (alphabetic)
            if ch.isalpha():
                func_name = ''
                while i < len(expression) and expression[i].isalpha():
                    func_name += expression[i]
                    i += 1
                tokens.append((self.FUNCTION, func_name))
                continue

            # Unknown/skip
            i += 1

        return tokens

    # Keep a regex-backed tokenizer available for tests or future reference
    def _tokenize_regex(self, expression: str) -> List[Tuple[str, str]]:
        tokens = []
        for match in re.finditer(self.pattern, expression):
            groups = match.groups()
            if groups[0]:
                tokens.append((self.NUMBER, groups[0]))
            elif groups[1]:
                tokens.append((self.OPERATOR, groups[1]))
            elif groups[2]:
                if groups[2] == '(':
                    tokens.append((self.LPAREN, groups[2]))
                else:
                    tokens.append((self.RPAREN, groups[2]))
            elif groups[3]:
                tokens.append((self.FUNCTION, groups[3]))
        return tokens