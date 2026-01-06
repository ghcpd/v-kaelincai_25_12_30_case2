"""
Tokenizer module — fixed version.
Fix: always use the context-aware tokenization that correctly handles
unary minus / negative literals. This preserves angle-mode behavior
while restoring negative-number handling (regression from v1.1).
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

        angle_mode is a semantic flag for the Calculator and should NOT
        change how numeric literals (including negative numbers) are
        tokenized. The regression in v1.1 accidentally made the
        tokenizer treat '-' as a standalone operator in angle mode —
        this file restores the context-aware behavior.
        """
        self.angle_mode = angle_mode

        # Single robust pattern is kept for potential simple matches but
        # we prefer the context-aware tokenizer below which correctly
        # handles unary minus, parentheses and function names.
        self._pattern = r'(-?\d+\.?\d*)|([+\-*/^])|([()])|([a-z]+)'

    def tokenize(self, expression: str) -> List[Tuple[str, str]]:
        """Tokenize a mathematical expression (context-aware).

        Important: tokenization must be identical whether or not
        angle_mode is enabled — angle_mode only affects function
        evaluation (degrees vs radians) in Calculator.
        """
        expression = expression.replace(' ', '')  # Remove whitespace
        # Always use the context-aware tokenizer to correctly handle
        # unary minus and negative literals (fixes regression).
        return self._tokenize_context_aware(expression)

    def _tokenize_context_aware(self, expression: str) -> List[Tuple[str, str]]:
        """Context-aware tokenization that properly recognizes unary minus."""
        tokens = []
        i = 0
        length = len(expression)

        while i < length:
            ch = expression[i]

            # Number (including a leading unary minus when appropriate)
            if ch.isdigit() or (ch == '-' and i + 1 < length and expression[i+1].isdigit() and
                                (i == 0 or expression[i-1] in '(+*/^-')):
                num_str = ''
                if ch == '-':
                    num_str = '-'
                    i += 1
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
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

            # Function names
            if ch.isalpha():
                func_name = ''
                while i < length and expression[i].isalpha():
                    func_name += expression[i]
                    i += 1
                tokens.append((self.FUNCTION, func_name))
                continue

            # Ignore any other characters (robustness)
            i += 1

        return tokens
