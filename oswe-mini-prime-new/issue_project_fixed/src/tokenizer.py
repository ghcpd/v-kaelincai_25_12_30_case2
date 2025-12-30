"""
Tokenizer module for mathematical expressions.
Handles lexical analysis and converts expression strings into tokens.
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
            angle_mode: If True, use angle mode for trigonometric functions (v1.1 feature)
        """
        self.angle_mode = angle_mode
        
        # Version 1.0 pattern (CORRECT - handles negative numbers properly)
        # This pattern treats -5 as a single NUMBER token
        self._pattern_v1_0 = r'(-?\d+\.?\d*)|([+*/^])|([()])|([a-z]+)'
        
        # Version 1.1 pattern (originally BUGGY - introduced when adding angle mode)
        # Fix: Include optional leading '-' in the NUMBER pattern so negative literals
        # remain a single NUMBER token even when angle_mode is enabled.
        self._pattern_v1_1 = r'(-?\d+\.?\d*)|([+\-*/^])|([()])|([a-z]+)'
        
        # Select pattern based on mode
        if angle_mode:
            self.pattern = self._pattern_v1_1  # FIXED VERSION for angle mode
        else:
            self.pattern = self._pattern_v1_0  # ORIGINAL WORKING VERSION
    
    def tokenize(self, expression: str) -> List[Tuple[str, str]]:
        """
        Tokenize a mathematical expression.
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            List of (token_type, token_value) tuples
        """
        expression = expression.replace(' ', '')  # Remove whitespace
        tokens = []
        
        if not self.angle_mode:
            # V1.0: Smart tokenization with context awareness
            return self._tokenize_v1_0(expression)
        else:
            # V1.1: Use regex-based tokenization (now fixed to handle negatives)
            return self._tokenize_v1_1(expression)
    
    def _tokenize_v1_0(self, expression: str) -> List[Tuple[str, str]]:
        """V1.0 tokenization - works correctly with negative numbers."""
        tokens = []
        i = 0
        
        while i < len(expression):
            ch = expression[i]
            
            # Check for numbers (including negative)
            if ch.isdigit() or (ch == '-' and i + 1 < len(expression) and expression[i+1].isdigit() and
                                (i == 0 or expression[i-1] in '(+*/^-')):  # Added '-' for double negative
                # This is a number (possibly negative)
                num_str = ''
                if ch == '-':
                    num_str = '-'
                    i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                tokens.append((self.NUMBER, num_str))
                continue
            
            # Check for operators
            if ch in '+-*/^':
                tokens.append((self.OPERATOR, ch))
                i += 1
                continue
            
            # Check for parentheses
            if ch == '(':
                tokens.append((self.LPAREN, ch))
                i += 1
                continue
            if ch == ')':
                tokens.append((self.RPAREN, ch))
                i += 1
                continue
            
            # Check for function names
            if ch.isalpha():
                func_name = ''
                while i < len(expression) and expression[i].isalpha():
                    func_name += expression[i]
                    i += 1
                tokens.append((self.FUNCTION, func_name))
                continue
            
            i += 1
        
        return tokens
    
    def _tokenize_v1_1(self, expression: str) -> List[Tuple[str, str]]:
        """V1.1 tokenization - uses regex but now handles negative numbers correctly."""
        tokens = []
        
        for match in re.finditer(self.pattern, expression):
            groups = match.groups()
            
            if groups[0]:  # Number (may be negative)
                tokens.append((self.NUMBER, groups[0]))
            elif groups[1]:  # Operator
                tokens.append((self.OPERATOR, groups[1]))
            elif groups[2]:  # Parentheses
                if groups[2] == '(':
                    tokens.append((self.LPAREN, groups[2]))
                else:
                    tokens.append((self.RPAREN, groups[2]))
            elif groups[3]:  # Function name
                tokens.append((self.FUNCTION, groups[3]))
        
        return tokens
