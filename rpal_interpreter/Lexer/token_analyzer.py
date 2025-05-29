"""
Token Analyzer Module for RPAL Interpreter
This module handles the lexical analysis (tokenization) of RPAL source code.
"""

import re
from enum import Enum, auto

class TokenCategory(Enum):
    """Enumeration of token categories in RPAL language."""
    KEYWORD = auto()
    IDENTIFIER = auto() 
    NUMBER = auto()
    TEXT = auto()
    OPERATOR = auto()
    PUNCTUATION = auto()
    EOF = auto()

class Token:
    """
    Represents a token in the RPAL language.
    
    Attributes:
        category (TokenCategory): The category of the token
        value (str): The string value of the token
        line (int): The line number where the token appears
        column (int): The column number where the token starts
    """
    
    def __init__(self, category, value, line=0, column=0):
        """
        Initialize a new Token instance.
        
        Args:
            category (TokenCategory): The category of the token
            value (str): The string value of the token
            line (int, optional): The line number where the token appears
            column (int, optional): The column number where the token starts
        """
        self.category = category
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        """Return a string representation of the token."""
        return f"<{self.category.name}, '{self.value}'>"
    
    def get_category(self):
        """Get the category of the token."""
        return self.category
    
    def get_value(self):
        """Get the string value of the token."""
        return self.value
    
    def get_position(self):
        """Get the position (line, column) of the token."""
        return (self.line, self.column)

def tokenize(source_code):
    """
    Convert RPAL source code into a list of tokens.
    
    Args:
        source_code (str): The RPAL source code to tokenize
        
    Returns:
        list: A list of Token objects
    """
    tokens = []
    line_num = 1
    position = 0
    
    # Process the entire source code as a single string
    while position < len(source_code):
        # Track line numbers
        if position < len(source_code) and source_code[position] == '\n':
            line_num += 1
            position += 1
            continue
        
        # Skip whitespace
        match = re.match(r'\s+', source_code[position:])
        if match:
            if '\n' in match.group():
                line_num += match.group().count('\n')
            position += match.end()
            continue
            
        # Check for comments
        if source_code[position:].startswith('//'):
            # Find the end of the line
            end_of_line = source_code.find('\n', position)
            if end_of_line == -1:  # No newline found
                position = len(source_code)  # Move to the end of the source
            else:
                position = end_of_line + 1
                line_num += 1
            continue
            
        # Try to match a token
        token = None
        
        # Check for text (strings) - must be checked before operators
        if position < len(source_code) and source_code[position] == "'":
            # Find the closing quote
            start_pos = position
            position += 1  # Skip the opening quote
            
            # Continue until we find a closing quote that's not escaped
            while position < len(source_code) and (source_code[position] != "'" or source_code[position-1] == '\\'):
                if source_code[position] == '\n':
                    line_num += 1
                position += 1
            
            if position < len(source_code) and source_code[position] == "'":
                # Include the closing quote
                position += 1
                token = Token(TokenCategory.TEXT, source_code[start_pos:position], line_num, start_pos + 1)
            else:
                raise ValueError(f"Unclosed string starting at line {line_num}, column {start_pos + 1}")
        
        # Check for keywords
        elif re.match(r'[a-zA-Z]', source_code[position:position+1]):
            word_match = re.match(r'[a-zA-Z][a-zA-Z0-9_]*', source_code[position:])
            word = word_match.group()
            
            if word in ["let", "in", "fn", "where", "aug", "or", "not", "gr", "ge", "ls", "le", "eq", "ne", 
                       "true", "false", "nil", "dummy", "within", "and", "rec"]:
                token = Token(TokenCategory.KEYWORD, word, line_num, position + 1)
            else:
                token = Token(TokenCategory.IDENTIFIER, word, line_num, position + 1)
            
            position += len(word)
        
        # Check for numbers
        elif re.match(r'[0-9]', source_code[position:position+1]):
            number_match = re.match(r'\d+', source_code[position:])
            token = Token(TokenCategory.NUMBER, number_match.group(), line_num, position + 1)
            position += number_match.end()
        
        # Check for multi-character operators
        elif position + 1 < len(source_code):
            if source_code[position:position+2] == '->':
                token = Token(TokenCategory.OPERATOR, '->', line_num, position + 1)
                position += 2
            elif source_code[position:position+2] == '>=':
                token = Token(TokenCategory.OPERATOR, '>=', line_num, position + 1)
                position += 2
            elif source_code[position:position+2] == '<=':
                token = Token(TokenCategory.OPERATOR, '<=', line_num, position + 1)
                position += 2
            elif source_code[position:position+2] == '==':
                token = Token(TokenCategory.OPERATOR, '==', line_num, position + 1)
                position += 2
            elif source_code[position:position+2] == '!=':
                token = Token(TokenCategory.OPERATOR, '!=', line_num, position + 1)
                position += 2
            elif source_code[position] == '=':
                token = Token(TokenCategory.OPERATOR, '=', line_num, position + 1)
                position += 1
            # Check for single-character operators
            elif source_code[position] in '+-*/<>&.@/:~|$#!%^_[]{}"\?':
                token = Token(TokenCategory.OPERATOR, source_code[position], line_num, position + 1)
                position += 1
            # Check for punctuation
            elif source_code[position] in '();,':
                token = Token(TokenCategory.PUNCTUATION, source_code[position], line_num, position + 1)
                position += 1
            else:
                raise ValueError(f"Unexpected character at line {line_num}, column {position + 1}: '{source_code[position]}'")
        
        # Handle single characters at the end of the file
        elif position < len(source_code):
            if source_code[position] == '=':
                token = Token(TokenCategory.OPERATOR, '=', line_num, position + 1)
                position += 1
            elif source_code[position] in '+-*/<>&.@/:~|$#!%^_[]{}"\?':
                token = Token(TokenCategory.OPERATOR, source_code[position], line_num, position + 1)
                position += 1
            elif source_code[position] in '();,':
                token = Token(TokenCategory.PUNCTUATION, source_code[position], line_num, position + 1)
                position += 1
            else:
                raise ValueError(f"Unexpected character at line {line_num}, column {position + 1}: '{source_code[position]}'")
        
        if token:
            tokens.append(token)
    
    # Add an EOF token
    tokens.append(Token(TokenCategory.EOF, "", line_num, position + 1))
    
    return tokens

# For testing the module independently
if __name__ == "__main__":
    test_code = "let x = 5 in x + 3"
    print(f"Testing tokenizer with: {test_code}")
    
    tokens = tokenize(test_code)
    
    print("\nTokens found:")
    for token in tokens:
        print(token)
