# RPAL Interpreter Usage Guide

## Overview
This is an implementation of an RPAL (Right-reference Pedagogical Algorithmic Language) interpreter in Python. The interpreter follows a standard compiler pipeline:

1. Lexical Analysis (Tokenization)
2. Parsing (Abstract Syntax Tree construction)
3. Standardization (AST transformation)
4. Execution (CSE Machine)

## Requirements
- Python 3.6 or higher

## Project Structure
```
rpal_interpreter/
├── Lexer/                  # Tokenization module
│   └── token_analyzer.py   # Converts source code to tokens
├── Parser/                 # Parsing module
│   └── syntax_parser.py    # Builds AST from tokens
├── Standardizer/           # AST standardization module
│   ├── tree_node.py        # Tree node representation
│   ├── tree.py             # Tree structure
│   └── tree_builder.py     # Builds standardized tree
├── CSEMachine/             # Execution module
│   ├── elements.py         # CSE Machine elements
│   ├── cse_builder.py      # Builds CSE Machine
│   └── cse_engine.py       # Executes RPAL programs
├── Inputs/                 # Test input files
├── rpal.py                 # Main entry point
├── Makefile                # Build system
└── design_document.md      # Design documentation
```

## Usage
To run the RPAL interpreter:

```bash
python rpal.py <source_file> [-ast] [-st]
```

Options:
- `-ast`: Display the Abstract Syntax Tree and exit
- `-st`: Display the Standardized Tree and exit

Example:
```bash
python rpal.py Inputs/t1.txt
```

## Features
- Full RPAL language support
- Abstract Syntax Tree visualization
- Standardized Tree visualization
- CSE Machine execution

## Example Programs
Several example RPAL programs are provided in the `Inputs/` directory:

- `t1.txt`: Simple conditional expression
- `t2.txt`: Another conditional expression
- `t3.txt`: Function definition and application
- And more...

## Troubleshooting
If you encounter any issues:
1. Ensure Python 3.6+ is installed
2. Check that the input file exists and contains valid RPAL code
3. Verify file permissions (the interpreter should have read access to the input file)
