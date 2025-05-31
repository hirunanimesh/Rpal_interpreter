import argparse
import sys
from Lexer.token_analyzer import tokenize
from Parser.syntax_parser import SyntaxParser
from Standardizer.tree_builder import TreeBuilder
from CSEMachine.cse_factory import CSEMachineFactory
from CSEMachine.csemachine import CSEMachine
from Parser.StringAst import StringAst

def main():
    """Main entry point for the RPAL interpreter."""
    print("RPAL Interpreter")
    # Set up command-line argument parsing
    arg_parser = argparse.ArgumentParser(
        description='RPAL Interpreter - Processes RPAL language programs',
    )
    
    arg_parser.add_argument(
        'source_file', 
        help='Path to the RPAL source file to interpret'
    )
    
    arg_parser.add_argument(
        '-ast', 
        action='store_true', 
        help='Display the Abstract Syntax Tree and exit'
    )
    
    arg_parser.add_argument(
        '-st', 
        action='store_true', 
        help='Display the Standardized Tree and exit'
    )
    
    # Parse command-line arguments
    args = arg_parser.parse_args()
    
    try:
        # Read the source file
        with open(args.source_file, 'r') as file:
            source_code = file.read()
        
        # Step 1: Tokenize the source code
        tokens = tokenize(source_code)

        if not tokens:
            raise ValueError("No tokens found in the source code. Error in tokenization.")
            
        
        # Step 2: Parse tokens into an Abstract Syntax Tree
        parser = SyntaxParser(tokens)


        ast_root = parser.parse()


        if ast_root is None:
            raise Exception("Parsing failed")

        # Convert AST to string representation for display or further processing
        #ast_strings = parser.convert_ast_to_string_ast()
        ast_strings_converter = StringAst(parser)
        ast_strings = ast_strings_converter.convert_ast_to_string_ast()
        

        # Display AST if requested
        if args.ast:
            print("Abstract Syntax Tree:")
            for line in ast_strings:
                print(line)
            return
        
        #Step 3: Build and standardize the tree
        tree_builder = TreeBuilder()
        std_tree = tree_builder.build_tree(ast_strings)
        std_tree.standardize()
        
        #Display standardized tree if requested
        if args.st:
            print("Standardized Tree:")
            std_tree.print_tree()
            return
        
        #Step 4: Build and execute the CSE machine
        cse_builder = CSEMachineFactory()
        cse_machine = cse_builder.get_cse_machine(std_tree)
        
        # Execute the program and print the result
        print("Output of the program is:")
        cse_machine.get_answer()
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{args.source_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
