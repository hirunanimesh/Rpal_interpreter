"""
CSE Machine Builder Module for RPAL Interpreter
This module builds a CSE Machine from a standardized Abstract Syntax Tree.
"""

from CSEMachine.elements import *
from CSEMachine.cse_engine import CSEEngine

class CSEBuilder:
    """
    Factory class for building a CSE Machine from a standardized Abstract Syntax Tree.
    """
    
    def __init__(self):
        """Initialize a new CSEBuilder instance."""
        self.delta_index = 0
        self.lambda_index = 0
        self.control = []
        self.identifiers = []
    
    def build_machine(self, tree):
        """
        Build a CSE Machine from a standardized Abstract Syntax Tree.
        
        Args:
            tree (StandardTree): The standardized Abstract Syntax Tree
            
        Returns:
            CSEEngine: The constructed CSE Machine
        """
        # Initialize the control structure, stack, and environment
        control = []
        stack = []
        environment = [Environment(0)]  # Start with the global environment
        
        # Build the control structure from the AST
        if tree.get_root():
            delta = self._build_control_structure(tree.get_root())
            control.extend(delta.symbols)
        
        # Create and return the CSE Machine
        return CSEEngine(control, stack, environment)
    
    def _build_control_structure(self, node):
        """
        Build a control structure from an AST node.
        
        Args:
            node (TreeNode): The AST node to process
            
        Returns:
            Delta: The constructed control structure
        """
        # Create a new delta for this control structure
        delta = Delta(self.delta_index)
        self.delta_index += 1
        
        # Process the node based on its type
        if node.get_data() == "lambda":
            # Handle lambda node
            lambda_node = Lambda(self.lambda_index)
            self.lambda_index += 1
            
            # Process the parameter (first child)
            param_node = node.get_children()[0]
            identifier = Identifier(param_node.get_data())
            lambda_node.identifiers.append(identifier)
            
            # Process the body (second child)
            body_node = node.get_children()[1]
            body_delta = self._build_control_structure(body_node)
            lambda_node.set_delta(body_delta)
            
            # Add the lambda to the control structure
            delta.symbols.append(lambda_node)
        
        elif node.get_data() == "gamma":
            # Handle gamma node (function application)
            # Process the function (first child)
            func_delta = self._build_control_structure(node.get_children()[0])
            delta.symbols.extend(func_delta.symbols)
            
            # Process the argument (second child)
            arg_delta = self._build_control_structure(node.get_children()[1])
            delta.symbols.extend(arg_delta.symbols)
            
            # Add the gamma operator
            delta.symbols.append(Gamma())
        
        elif node.get_data() == "->":
            # Handle conditional node
            # Process the condition (first child)
            cond_delta = self._build_control_structure(node.get_children()[0])
            delta.symbols.extend(cond_delta.symbols)
            
            # Create a beta control structure
            beta = Beta()
            
            # Process the true branch (second child)
            true_delta = self._build_control_structure(node.get_children()[1])
            beta.symbols.append(true_delta)
            
            # Process the false branch (third child)
            false_delta = self._build_control_structure(node.get_children()[2])
            beta.symbols.append(false_delta)
            
            # Add the beta to the control structure
            delta.symbols.append(beta)
        
        elif node.get_data() == "tau":
            # Handle tuple constructor
            n = len(node.get_children())
            
            # Process each element in the tuple
            for child in node.get_children():
                child_delta = self._build_control_structure(child)
                delta.symbols.extend(child_delta.symbols)
            
            # Add the tau operator
            delta.symbols.append(Tau(n))
        
        elif node.get_data() == "=":
            # Handle assignment
            # Process the right-hand side (second child)
            rhs_delta = self._build_control_structure(node.get_children()[1])
            delta.symbols.extend(rhs_delta.symbols)
            
            # Process the left-hand side (first child) - should be an identifier
            lhs_node = node.get_children()[0]
            if lhs_node.get_data().startswith("<"):
                # Handle special node format
                parts = lhs_node.get_data().strip("<>").split(":")
                if len(parts) > 1:
                    identifier = Identifier(parts[1])
                else:
                    identifier = Identifier(parts[0])
            else:
                identifier = Identifier(lhs_node.get_data())
            
            # Add the identifier to the control structure
            delta.symbols.append(identifier)
        
        elif node.get_data() == "<Y*>":
            # Handle Y* (fixed-point combinator)
            delta.symbols.append(Ystar())
        
        elif node.get_data() in ["+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"]:
            # Handle binary operators
            # Process the left operand (first child)
            left_delta = self._build_control_structure(node.get_children()[0])
            delta.symbols.extend(left_delta.symbols)
            
            # Process the right operand (second child)
            right_delta = self._build_control_structure(node.get_children()[1])
            delta.symbols.extend(right_delta.symbols)
            
            # Add the operator
            delta.symbols.append(BinaryOperator(node.get_data()))
        
        elif node.get_data() in ["neg", "not"]:
            # Handle unary operators
            # Process the operand
            operand_delta = self._build_control_structure(node.get_children()[0])
            delta.symbols.extend(operand_delta.symbols)
            
            # Add the operator
            delta.symbols.append(UnaryOperator(node.get_data()))
        
        elif node.get_data().startswith("<IDENTIFIER:"):
            # Handle identifier node
            identifier_value = node.get_data().split(":")[1].rstrip(">")
            delta.symbols.append(Identifier(identifier_value))
        
        elif node.get_data().startswith("<NUMBER:"):
            # Handle number node
            number_value = node.get_data().split(":")[1].rstrip(">")
            delta.symbols.append(Integer(number_value))
        
        elif node.get_data().startswith("<TEXT:"):
            # Handle text node
            text_value = node.get_data().split(":")[1].rstrip(">")
            delta.symbols.append(Text(text_value))
        
        elif node.get_data() == "true":
            # Handle true value
            delta.symbols.append(Boolean("true"))
        
        elif node.get_data() == "false":
            # Handle false value
            delta.symbols.append(Boolean("false"))
        
        elif node.get_data() == "nil":
            # Handle nil value
            delta.symbols.append(Nil())
        
        elif node.get_data() == "dummy":
            # Handle dummy value
            delta.symbols.append(Dummy())
        
        else:
            # Handle other nodes (likely identifiers)
            delta.symbols.append(Identifier(node.get_data()))
        
        return delta
