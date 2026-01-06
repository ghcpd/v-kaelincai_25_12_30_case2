"""
Scientific Calculator - Main calculator module (fixed copy).

This file is copied from the original project but uses the fixed Tokenizer in
this package's `src/tokenizer.py`.
"""

import math
import sys
import os
from typing import Union

# Add parent directory to path for imports (keeps same behavior as original)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tokenizer import Tokenizer


class Calculator:
    """
    A scientific calculator supporting basic operations and scientific functions.
    """

    FUNCTIONS = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
    }

    def __init__(self):
        """Initialize calculator."""
        self.angle_mode = False  # Default to radian mode

    def set_angle_mode(self, use_degrees: bool):
        """Set trigonometric function mode."""
        self.angle_mode = use_degrees

    def calculate(self, expression: str) -> float:
        """Calculate the result of a mathematical expression."""
        tokenizer = Tokenizer(angle_mode=self.angle_mode)
        tokens = tokenizer.tokenize(expression)

        if not tokens:
            raise ValueError("Empty expression")

        postfix = self._infix_to_postfix(tokens)
        result = self._evaluate_postfix(postfix)

        return result

    def _infix_to_postfix(self, tokens):
        output = []
        operator_stack = []

        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        right_associative = {'^'}

        i = 0
        while i < len(tokens):
            token_type, token_value = tokens[i]

            if token_type == Tokenizer.NUMBER:
                output.append((token_type, token_value))

            elif token_type == Tokenizer.FUNCTION:
                operator_stack.append((token_type, token_value))

            elif token_type == Tokenizer.OPERATOR:
                while (operator_stack and 
                       operator_stack[-1][0] == Tokenizer.OPERATOR and
                       ((token_value not in right_associative and 
                         precedence.get(operator_stack[-1][1], 0) >= precedence[token_value]) or
                        (token_value in right_associative and 
                         precedence.get(operator_stack[-1][1], 0) > precedence[token_value]))):
                    output.append(operator_stack.pop())
                operator_stack.append((token_type, token_value))

            elif token_type == Tokenizer.LPAREN:
                operator_stack.append((token_type, token_value))

            elif token_type == Tokenizer.RPAREN:
                while operator_stack and operator_stack[-1][0] != Tokenizer.LPAREN:
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()
                if operator_stack and operator_stack[-1][0] == Tokenizer.FUNCTION:
                    output.append(operator_stack.pop())

            i += 1

        while operator_stack:
            if operator_stack[-1][0] == Tokenizer.LPAREN:
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        return output

    def _evaluate_postfix(self, postfix):
        stack = []

        for token_type, token_value in postfix:
            if token_type == Tokenizer.NUMBER:
                stack.append(float(token_value))

            elif token_type == Tokenizer.OPERATOR:
                if len(stack) < 2:
                    raise ValueError(f"Invalid expression: not enough operands for '{token_value}'")

                b = stack.pop()
                a = stack.pop()

                if token_value == '+':
                    stack.append(a + b)
                elif token_value == '-':
                    stack.append(a - b)
                elif token_value == '*':
                    stack.append(a * b)
                elif token_value == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
                elif token_value == '^':
                    stack.append(a ** b)

            elif token_type == Tokenizer.FUNCTION:
                if len(stack) < 1:
                    raise ValueError(f"Invalid expression: not enough arguments for '{token_value}'")

                arg = stack.pop()

                if token_value in self.FUNCTIONS:
                    func = self.FUNCTIONS[token_value]
                    if self.angle_mode and token_value in ['sin', 'cos', 'tan']:
                        arg = math.radians(arg)
                    try:
                        result = func(arg)
                        stack.append(result)
                    except (ValueError, ZeroDivisionError) as e:
                        raise ValueError(f"Math error in {token_value}({arg}): {e}")
                else:
                    raise ValueError(f"Unknown function: {token_value}")

        if len(stack) != 1:
            raise ValueError("Invalid expression: too many operands")

        return stack[0]


def main():
    calc = Calculator()
    print("Scientific Calculator (fixed)")
    calc.set_angle_mode(False)
    examples = ["-5 + 3", "2 * (-3)", "10 - -5", "sin(30)"]
    for expr in examples:
        try:
            print(f"{expr} = {calc.calculate(expr)}")
        except Exception as e:
            print(f"{expr} ERROR: {e}")


if __name__ == '__main__':
    main()