#!/usr/bin/env python3

.PHONY: clean run run-ast run-st

# Python interpreter
PYTHON = python

# Source files
SRC = myrpal.py

# Default target
all: clean

# Run the RPAL interpreter
run:
	$(PYTHON) $(SRC) $(SOURCE)

# Run with AST display
run-ast:
	$(PYTHON) $(SRC) $(SOURCE) -ast

# Run with Standardized Tree display
run-st:
	$(PYTHON) $(SRC) $(SOURCE) -st

# Clean up Python cache files and other temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +

# Install dependencies
install:
	pip install -r requirements.txt

# Help target
help:
	@echo "Available targets:"
	@echo "  all     - Clean the project"
	@echo "  run     - Run the RPAL interpreter (requires SOURCE=path/to/file.rpal)"
	@echo "  run-ast - Run and display Abstract Syntax Tree (requires SOURCE=path/to/file.rpal)"
	@echo "  run-st  - Run and display Standardized Tree (requires SOURCE=path/to/file.rpal)"
	@echo "  clean   - Remove Python cache files and temporary files"
	@echo "  install - Install dependencies"
