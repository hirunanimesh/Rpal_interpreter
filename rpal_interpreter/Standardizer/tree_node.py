"""
Tree Node Module for RPAL Interpreter
This module defines the node structure for the Abstract Syntax Tree.
"""

class TreeNode:
    """
    Represents a node in the Abstract Syntax Tree.
    
    Attributes:
        data (str): The data/value stored in the node
        depth (int): The depth of the node in the tree
        parent (TreeNode): The parent node
        children (list): List of child nodes
        is_standardized (bool): Whether the node has been standardized
    """
    
    def __init__(self):
        """Initialize a new TreeNode instance."""
        self.data = None
        self.depth = 0
        self.parent = None
        self.children = []
        self.is_standardized = False
    
    def set_data(self, data):
        """Set the data/value of the node."""
        self.data = data
    
    def get_data(self):
        """Get the data/value of the node."""
        return self.data
    
    def get_degree(self):
        """Get the number of children (degree) of the node."""
        return len(self.children)
    
    def get_children(self):
        """Get the list of child nodes."""
        return self.children
    
    def set_depth(self, depth):
        """Set the depth of the node in the tree."""
        self.depth = depth
    
    def get_depth(self):
        """Get the depth of the node in the tree."""
        return self.depth
    
    def set_parent(self, parent):
        """Set the parent node."""
        self.parent = parent
    
    def get_parent(self):
        """Get the parent node."""
        return self.parent
    
    def standardize(self):
        """
        Standardize the node and its subtree according to RPAL transformation rules.
        This method applies the appropriate standardization rule based on the node's data.
        """
        if self.is_standardized:
            return
        
        # First standardize all children
        for child in self.children:
            child.standardize()
        
        # Apply standardization rules based on node type
        if self.data == "let":
            self._standardize_let()
        elif self.data == "where":
            self._standardize_where()
        elif self.data == "function_form":
            self._standardize_function_form()
        elif self.data == "lambda":
            self._standardize_lambda()
        elif self.data == "within":
            self._standardize_within()
        elif self.data == "@":
            self._standardize_at()
        elif self.data == "and":
            self._standardize_and()
        elif self.data == "rec":
            self._standardize_rec()
        
        self.is_standardized = True
    
    def _standardize_let(self):
        """
        Standardize a 'let' node.
        
        Transformation:
            LET              GAMMA
           /   \            /     \
          EQUAL  P   ->   LAMBDA   E
         /    \          /    \
        X      E        X      P
        """
        # Extract components
        equal_node = self.children[0]
        p_node = self.children[1]
        
        # Rearrange nodes
        temp1 = equal_node.children[1]  # E
        temp1.set_parent(self)
        temp1.set_depth(self.depth + 1)
        
        temp2 = p_node  # P
        temp2.set_parent(equal_node)
        temp2.set_depth(self.depth + 2)
        
        self.children[1] = temp1
        equal_node.set_data("lambda")
        equal_node.children[1] = temp2
        self.set_data("gamma")
    
    def _standardize_where(self):
        """
        Standardize a 'where' node.
        
        Transformation:
            WHERE               LET
           /    \             /     \
          P     EQUAL   ->  EQUAL    P
                /   \       /   \
               X     E     X     E
        """
        # Swap children
        temp = self.children[0]
        self.children[0] = self.children[1]
        self.children[1] = temp
        
        # Change node type and re-standardize
        self.set_data("let")
        self.standardize()  # Apply let standardization
    
    def _standardize_function_form(self):
        """
        Standardize a 'function_form' node.
        
        Transformation:
            FCN_FORM                EQUAL
           /   |   \               /    \
          P    V+   E    ->       P     +LAMBDA
                                        /     \
                                       V      .E
        """
        # Extract components
        p_node = self.children[0]  # P (function name)
        e_node = self.children[-1]  # E (function body)
        
        # Create lambda node
        current_lambda = NodeFactory.create_node_with_parent("lambda", self.depth + 1, self, [], True)
        self.children.insert(1, current_lambda)
        
        # Process variable bindings
        i = 2
        while self.children[i] != e_node:
            v_node = self.children[i]
            self.children.pop(i)
            v_node.set_depth(current_lambda.depth + 1)
            v_node.set_parent(current_lambda)
            current_lambda.children.append(v_node)
            
            # Create nested lambda if more variables exist
            if len(self.children) > 3:
                new_lambda = NodeFactory.create_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                current_lambda.children.append(new_lambda)
                current_lambda = new_lambda
        
        # Add function body to innermost lambda
        current_lambda.children.append(e_node)
        self.children.pop(2)  # Remove E from original position
        
        # Change node type
        self.set_data("=")
    
    def _standardize_lambda(self):
        """
        Standardize a 'lambda' node with multiple variables.
        
        Transformation:
            LAMBDA        LAMBDA
           /   |   \  ->  /    \
          V1   V2   E    V1    LAMBDA
                                /    \
                               V2     E
        """
        if len(self.children) > 2:
            e_node = self.children[-1]  # Function body
            
            # Create first nested lambda
            current_lambda = NodeFactory.create_node_with_parent("lambda", self.depth + 1, self, [], True)
            self.children.insert(1, current_lambda)
            
            # Process variable bindings
            i = 2
            while self.children[i] != e_node:
                v_node = self.children[i]
                self.children.pop(i)
                v_node.set_depth(current_lambda.depth + 1)
                v_node.set_parent(current_lambda)
                current_lambda.children.append(v_node)
                
                # Create nested lambda if more variables exist
                if len(self.children) > 3:
                    new_lambda = NodeFactory.create_node_with_parent("lambda", current_lambda.depth + 1, current_lambda, [], True)
                    current_lambda.children.append(new_lambda)
                    current_lambda = new_lambda
            
            # Add function body to innermost lambda
            current_lambda.children.append(e_node)
            self.children.pop(2)  # Remove E from original position
    
    def _standardize_within(self):
        """
        Standardize a 'within' node.
        
        Transformation:
            WITHIN                  EQUAL
           /      \                /     \
         EQUAL   EQUAL    ->      X2     GAMMA
        /    \   /    \                  /    \
       X1    E1 X2    E2               LAMBDA  E1
                                       /    \
                                      X1    E2
        """
        # Extract components
        x1_node = self.children[0].children[0]
        x2_node = self.children[1].children[0]
        e1_node = self.children[0].children[1]
        e2_node = self.children[1].children[1]
        
        # Create new nodes
        gamma_node = NodeFactory.create_node_with_parent("gamma", self.depth + 1, self, [], True)
        lambda_node = NodeFactory.create_node_with_parent("lambda", self.depth + 2, gamma_node, [], True)
        
        # Adjust depths and parents
        x1_node.set_depth(x1_node.get_depth() + 1)
        x1_node.set_parent(lambda_node)
        
        x2_node.set_depth(x1_node.get_depth() - 1)
        x2_node.set_parent(self)
        
        e1_node.set_depth(e1_node.get_depth())
        e1_node.set_parent(gamma_node)
        
        e2_node.set_depth(e2_node.get_depth() + 1)
        e2_node.set_parent(lambda_node)
        
        # Build new structure
        lambda_node.children.append(x1_node)
        lambda_node.children.append(e2_node)
        
        gamma_node.children.append(lambda_node)
        gamma_node.children.append(e1_node)
        
        self.children.clear()
        self.children.append(x2_node)
        self.children.append(gamma_node)
        
        self.set_data("=")
    
    def _standardize_at(self):
        """
        Standardize an '@' node.
        
        Transformation:
            AT              GAMMA
           / | \    ->      /    \
          E1 N E2          GAMMA   E2
                          /    \
                         N     E1
        """
        # Extract components
        e1_node = self.children[0]
        n_node = self.children[1]
        e2_node = self.children[2]
        
        # Create new gamma node
        gamma1_node = NodeFactory.create_node_with_parent("gamma", self.depth + 1, self, [], True)
        
        # Adjust depths and parents
        e1_node.set_depth(e1_node.get_depth() + 1)
        e1_node.set_parent(gamma1_node)
        
        n_node.set_depth(n_node.get_depth() + 1)
        n_node.set_parent(gamma1_node)
        
        # Build new structure
        gamma1_node.children.append(n_node)
        gamma1_node.children.append(e1_node)
        
        self.children.pop(0)
        self.children.pop(0)
        self.children.insert(0, gamma1_node)
        
        self.set_data("gamma")
    
    def _standardize_and(self):
        """
        Standardize an 'and' node.
        
        Transformation:
            SIMULTDEF            EQUAL
                |               /     \
              EQUAL++  ->     COMMA   TAU
              /   \             |      |
             X     E           X++    E++
        """
        # Create new nodes
        comma_node = NodeFactory.create_node_with_parent(",", self.depth + 1, self, [], True)
        tau_node = NodeFactory.create_node_with_parent("tau", self.depth + 1, self, [], True)
        
        # Process each equal node
        for equal_node in self.children:
            # Extract X and E from each equal node
            x_node = equal_node.children[0]
            e_node = equal_node.children[1]
            
            # Adjust parents
            x_node.set_parent(comma_node)
            e_node.set_parent(tau_node)
            
            # Add to new structure
            comma_node.children.append(x_node)
            tau_node.children.append(e_node)
        
        # Replace children with new structure
        self.children.clear()
        self.children.append(comma_node)
        self.children.append(tau_node)
        
        self.set_data("=")
    
    def _standardize_rec(self):
        """
        Standardize a 'rec' node.
        
        Transformation:
            REC                 EQUAL
             |                 /     \
           EQUAL     ->       X     GAMMA
          /     \                   /    \
         X       E                YSTAR  LAMBDA
                                         /     \
                                         X      E
        """
        # Extract components
        x_node = self.children[0].children[0]
        e_node = self.children[0].children[1]
        
        # Create new nodes
        f_node = NodeFactory.create_node_with_parent(x_node.get_data(), self.depth + 1, self, x_node.children.copy(), True)
        g_node = NodeFactory.create_node_with_parent("gamma", self.depth + 1, self, [], True)
        y_node = NodeFactory.create_node_with_parent("<Y*>", self.depth + 2, g_node, [], True)
        l_node = NodeFactory.create_node_with_parent("lambda", self.depth + 2, g_node, [], True)
        
        # Adjust depths and parents
        x_node.set_depth(l_node.depth + 1)
        x_node.set_parent(l_node)
        
        e_node.set_depth(l_node.depth + 1)
        e_node.set_parent(l_node)
        
        # Build new structure
        l_node.children.append(x_node)
        l_node.children.append(e_node)
        
        g_node.children.append(y_node)
        g_node.children.append(l_node)
        
        self.children.clear()
        self.children.append(f_node)
        self.children.append(g_node)
        
        self.set_data("=")


class NodeFactory:
    """Factory class for creating TreeNode instances."""
    
    @staticmethod
    def create_node(data, depth):
        """
        Create a new TreeNode with the specified data and depth.
        
        Args:
            data (str): The data/value for the node
            depth (int): The depth of the node in the tree
            
        Returns:
            TreeNode: A new TreeNode instance
        """
        node = TreeNode()
        node.set_data(data)
        node.set_depth(depth)
        node.children = []
        return node
    
    @staticmethod
    def create_node_with_parent(data, depth, parent, children, is_standardized):
        """
        Create a new TreeNode with the specified attributes.
        
        Args:
            data (str): The data/value for the node
            depth (int): The depth of the node in the tree
            parent (TreeNode): The parent node
            children (list): List of child nodes
            is_standardized (bool): Whether the node is already standardized
            
        Returns:
            TreeNode: A new TreeNode instance
        """
        node = TreeNode()
        node.set_data(data)
        node.set_depth(depth)
        node.set_parent(parent)
        node.children = children
        node.is_standardized = is_standardized
        return node
