"""
Tree Builder Module for RPAL Interpreter
This module builds a standardized Abstract Syntax Tree from string representation.
"""

from Standardizer.tree_node import TreeNode, NodeFactory
from Standardizer.tree import StandardTree

class TreeBuilder:
    """
    Factory class for building a standardized Abstract Syntax Tree.
    """
    
    def __init__(self):
        """Initialize a new TreeBuilder instance."""
        pass
    
    def build_tree(self, string_representation):
        """
        Build a StandardTree from a string representation of an AST.
        
        Args:
            string_representation (list): List of strings representing the AST
            
        Returns:
            StandardTree: The constructed tree
        """
        if not string_representation:
            return StandardTree()
        
        
        
        # Create the root node
        root = NodeFactory.create_node(string_representation[0], 0)
        
        
        # Initialize tracking variables
        previous_node = root
        current_depth = 0
        
        # Process each line in the string representation
        for line in string_representation[1:]:
            # Count the depth (number of dots)
            i = 0
            depth = 0
            while i < len(line) and line[i] == '.':
                depth += 1
                i += 1
            
            # Extract the node data
            
            node_data = line[i:]
            
            
            # Connect the node to the tree
            current_node = NodeFactory.create_node(node_data, depth)
            if current_depth < depth:
                # This is a child of the previous node
                previous_node.children.append(current_node)
                current_node.set_parent(previous_node)
            else:
                # Find the appropriate parent by traversing up the tree
                temp_node = previous_node
                while temp_node.get_depth() != depth - 1:
                    temp_node = temp_node.get_parent()
                
                # Add as a child of the found parent
                temp_node.children.append(current_node)
                current_node.set_parent(temp_node)
            
            # Update tracking variables for the next iteration
            previous_node = current_node
            current_depth = depth
        
        # Create and return the StandardTree
        return StandardTree(root)
    
    def _parse_special_node(self, node_data):
        """
        Parse a special node with type:value format.
        
        Args:
            node_data (str): The node data string in format <TYPE:VALUE>
            
        Returns:
            tuple: (type, value) extracted from the node data
        """
        # Remove the angle brackets
        content = node_data.strip('<>')
        
        # Split by colon
        parts = content.split(':', 1)
        
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            # If no colon, return the whole content as both type and value
            return content, content
