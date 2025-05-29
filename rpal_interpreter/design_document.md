# RPAL Interpreter Design Document

## Overview
This document outlines the design for an RPAL (Right-reference Pedagogical Algorithmic Language) interpreter implemented in Python. The interpreter follows a standard compiler/interpreter pipeline with four main components:

1. **Lexical Analyzer (Tokenizer)** - Converts source code into tokens
2. **Parser** - Builds an Abstract Syntax Tree (AST) from tokens
3. **Standardizer** - Transforms the AST into a standardized form
4. **CSE Machine** - Executes the standardized AST

## File Structure
```
rpal_interpreter/
├── Lexer/
│   └── token_analyzer.py
├── Parser/
│   └── syntax_parser.py
├── Standardizer/
│   ├── tree.py
│   ├── tree_node.py
│   └── tree_builder.py
├── CSEMachine/
│   ├── cse_engine.py
│   ├── cse_builder.py
│   └── elements.py
├── Inputs/
│   └── (test files)
├── rpal.py (main entry point)
└── Makefile
```

## Component Design

### 1. Lexical Analyzer (Tokenizer)
**File**: `Lexer/token_analyzer.py`

**Key Classes**:
- `TokenCategory` - Enum for token types (KEYWORD, IDENTIFIER, NUMBER, TEXT, OPERATOR, PUNCTUATION, EOF)
- `Token` - Class to represent tokens with category and value
- `Tokenizer` - Class to convert source code into tokens

**Key Methods**:
- `tokenize(source_code)` - Converts source text into a list of tokens
- `is_keyword(text)`, `is_identifier(text)`, etc. - Helper methods for token classification

**Design Differences**:
- Use of regular expressions with named capture groups instead of sequential matching
- Different naming convention for token types and methods
- Implementation of a state-based tokenizer instead of regex-only approach
- Enhanced error reporting with line and column information

### 2. Parser
**File**: `Parser/syntax_parser.py`

**Key Classes**:
- `NodeKind` - Enum for AST node types
- `ASTNode` - Class to represent nodes in the AST
- `SyntaxParser` - Class to build AST from tokens using recursive descent

**Key Methods**:
- `parse()` - Entry point for parsing
- `expression()`, `term()`, etc. - Methods for parsing grammar rules
- `ast_to_string_representation()` - Converts AST to string representation

**Design Differences**:
- Different recursive descent implementation with predictive parsing
- Use of visitor pattern for AST traversal
- Different method names and organization
- Enhanced error handling with specific error messages
- Different approach to handling operator precedence

### 3. Standardizer
**Files**:
- `Standardizer/tree.py` - Abstract Syntax Tree representation
- `Standardizer/tree_node.py` - Node implementation for the AST
- `Standardizer/tree_builder.py` - Builds standardized AST

**Key Classes**:
- `TreeNode` - Base class for AST nodes
- `StandardTree` - Class representing the standardized AST
- `TreeBuilder` - Factory class to build the standardized AST

**Key Methods**:
- `standardize()` - Transforms AST into standardized form
- `transform_let()`, `transform_where()`, etc. - Methods for specific transformations
- `print_tree()` - Displays the standardized tree

**Design Differences**:
- Different approach to tree transformation using visitor pattern
- Different naming convention for transformation methods
- Implementation of tree traversal using iterative approach instead of recursive
- Different node structure and inheritance hierarchy

### 4. CSE Machine
**Files**:
- `CSEMachine/cse_engine.py` - Main CSE machine implementation
- `CSEMachine/cse_builder.py` - Builds CSE machine from standardized AST
- `CSEMachine/elements.py` - Elements used in CSE machine

**Key Classes**:
- `Element` - Base class for CSE machine elements
- `CSEEngine` - Main execution engine
- `CSEBuilder` - Factory class to build CSE machine

**Key Methods**:
- `evaluate()` - Executes the CSE machine
- `apply_operation()` - Applies operations to operands
- `get_result()` - Returns the final result

**Design Differences**:
- Different control flow for execution
- Different naming convention for CSE machine elements
- Implementation of environment using dictionaries with parent references
- Different approach to handling operations and function application

### 5. Main Entry Point
**File**: `rpal.py`

**Key Functions**:
- `main()` - Entry point for the interpreter
- `process_file(filename)` - Processes an RPAL source file
- Command-line argument handling with argparse

**Design Differences**:
- Different organization of the main function
- Enhanced error handling and reporting
- Different command-line options and help messages
- Implementation of additional debugging features

## Implementation Strategy
1. Implement each component separately, ensuring they work correctly in isolation
2. Integrate components one by one, testing at each step
3. Validate against test cases from the Inputs directory
4. Refine and optimize as needed

## Testing Strategy
1. Unit tests for each component
2. Integration tests for component interactions
3. End-to-end tests using provided test cases
4. Comparison with reference implementation output
