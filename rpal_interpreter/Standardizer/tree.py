"""
Tree Module for RPAL Interpreter
This module defines the Abstract Syntax Tree structure.
"""

from Standardizer.tree_node import TreeNode

class StandardTree:
    """
    Represents an Abstract Syntax Tree for RPAL programs.
    
    Attributes:
        root (TreeNode): The root node of the tree
    """
    
    def __init__(self, root=None):
        """
        Initialize a new StandardTree.
        
        Args:
            root (TreeNode, optional): The root node of the tree
        """
        self.root = root
    
    def set_root(self, root):
        """Set the root node of the tree."""
        self.root = root
    
    def get_root(self):
        """Get the root node of the tree."""
        return self.root
    
    def standardize(self):
        """
        Standardize the tree by applying transformation rules.
        This process converts the AST into a standardized form suitable for execution.
        """
        if self.root and not self.root.is_standardized:
            self.root.standardize()
    
    def pre_order_traverse(self, node, indent_level):
        """
        Traverse the tree in pre-order and print each node.
        
        Args:
            node (TreeNode): The current node being visited
            indent_level (int): The current indentation level
        """
        # Print the node's data with indentation based on the level
        print(node.get_data())
        print("." * indent_level + str(node.get_data()))
        
        # Traverse through each child node recursively
        for child in node.children:
            self.pre_order_traverse(child, indent_level + 1)
    
    def print_tree(self):
        """Print the entire tree in a hierarchical format."""
        if self.root:
            self.pre_order_traverse(self.root, 0)
        else:
            print("Empty tree")
