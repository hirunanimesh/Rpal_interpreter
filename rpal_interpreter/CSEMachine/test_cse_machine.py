"""
Test script for validating the CSE Machine implementation
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('/home/ubuntu/lexer_parser_files')
sys.path.append('/home/ubuntu/lexer_parser_files/Lexer and parser')

from Lexer.token_analyzer import tokenize
from Parser.syntax_parser import SyntaxParser
from standerizer.tree_builder import TreeBuilder
from standerizer.tree import StandardTree
from cse_implementation.cse_factory import CSEMachineFactory

def test_cse_machine(source_code):
    """
    Test the CSE Machine with the given source code
    
    Args:
        source_code (str): RPAL source code to test
        
    Returns:
        str: The result of executing the code
    """
    print("Testing CSE Machine with source code:")
    print(source_code)
    print("\nTokenizing...")
    
    # Tokenize the source code
    tokens = tokenize(source_code)
    
    print("Parsing...")
    # Parse the tokens into an AST
    parser = SyntaxParser(tokens)
    ast = parser.parse()
    
    if ast is None:
        print("Parsing failed!")
        return None
    
    print("Converting to string representation...")
    # Convert the AST to string representation
    string_ast = parser.convert_ast_to_string_ast()
    
    print("Building standardized tree...")
    # Build a standardized tree from the string representation
    tree_builder = TreeBuilder()
    tree = tree_builder.build_tree(string_ast)
    
    print("Standardizing tree...")
    # Standardize the tree
    tree.standardize()
    
    print("Creating CSE Machine...")
    # Create a CSE Machine from the standardized tree
    factory = CSEMachineFactory()
    cse_machine = factory.get_cse_machine(tree)
    
    print("Executing CSE Machine...")
    # Execute the CSE Machine and get the result
    result = cse_machine.get_answer()
    
    print("Result:", result)
    return result

# Test cases
test_cases = [
    "let x = 5 in x + 3",
    "let f = fn x.x+1 in f 5",
    "let fact = rec f.fn n.eq n 0 -> 1 | n * f(n-1) in fact 5"
]

# Run test cases
for i, test_case in enumerate(test_cases):
    print(f"\n=== Test Case {i+1} ===")
    result = test_cse_machine(test_case)
    print("=" * 40)

print("\nAll tests completed!")
