
from .symbols import *
from .csemachine import CSEMachine

class CSEMachineFactory:
    """
    Factory class for creating CSE Machine instances from standardized trees
    """
    def __init__(self):
        """Initialize a new CSEMachineFactory instance"""
        self.e0 = E(0)
        self.i = 1  # Lambda index counter
        self.j = 0  # Delta index counter

    def get_symbol(self, node):
        """
        Convert a tree node to the appropriate CSE Machine symbol
        
        Args:
            node: A node from the standardized tree
            
        Returns:
            Symbol: The corresponding CSE Machine symbol
        """
        data = node.get_data()
        
        # Handle operators
        if data in ("not", "neg"):
            return Uop(data)  # Unary operator symbol
        elif data in ("+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"):
            return Bop(data)  # Binary operator symbol
        elif data == "gamma":
            return Gamma()  # Gamma symbol
        elif data == "tau":
            return Tau(len(node.get_children()))  # Tau symbol with the number of children
        elif data == "<Y*>":
            return Ystar()  # Y* symbol
        else:
            # Handle special node types (identifiers, literals, etc.)
            if data.startswith("<IDENTIFIER:"):
                return Id(data[12:-1])  # Identifier symbol
            elif data.startswith("<INTEGER:"):
                return Int(data[9:-1])  # Integer symbol
            elif data.startswith("<STRING:"):
                return Str(data[9:-2])  # String symbol (remove quotes)
            elif data.startswith("<NIL"):
                return Tup()  # Empty tuple symbol
            elif data.startswith("<TRUE_VALUE:t"):
                return Bool("true")  # Boolean true symbol
            elif data.startswith("<TRUE_VALUE:f"):
                return Bool("false")  # Boolean false symbol
            elif data.startswith("<dummy>"):
                return Dummy()  # Dummy symbol
            else:
                print("Error: Unknown node type:", data)
                return Err()  # Error symbol

    def get_b(self, node):
        """
        Create a B symbol (conditional block) from a tree node
        
        Args:
            node: A node from the standardized tree
            
        Returns:
            B: A B symbol with its symbols list populated
        """
        b = B()
        b.symbols = self.get_pre_order_traverse(node)
        return b

    def get_lambda(self, node):
        """
        Create a Lambda symbol from a tree node
        
        Args:
            node: A lambda node from the standardized tree
            
        Returns:
            Lambda: A Lambda symbol with its properties set
        """
        lambda_expr = Lambda(self.i)
        self.i += 1
        lambda_expr.set_delta(self.get_delta(node.get_children()[1]))
        
        # Handle parameter list
        if node.get_children()[0].get_data() == ",":
            for identifier in node.get_children()[0].get_children():
                lambda_expr.identifiers.append(Id(identifier.get_data()[12:-1]))
        else:
            lambda_expr.identifiers.append(Id(node.get_children()[0].get_data()[12:-1]))
            
        return lambda_expr

    def get_pre_order_traverse(self, node):
        """
        Traverse a tree node in pre-order and convert to CSE Machine symbols
        
        Args:
            node: A node from the standardized tree
            
        Returns:
            list: A list of CSE Machine symbols
        """
        symbols = []
        
        if node.get_data() == "lambda":
            symbols.append(self.get_lambda(node))  # Lambda expression symbol
        elif node.get_data() == "->":
            symbols.append(self.get_delta(node.get_children()[1]))  # Then branch
            symbols.append(self.get_delta(node.get_children()[2]))  # Else branch
            symbols.append(Beta())  # Beta symbol for branching
            symbols.append(self.get_b(node.get_children()[0]))  # Condition
        else:
            symbols.append(self.get_symbol(node))
            for child in node.get_children():
                symbols.extend(self.get_pre_order_traverse(child))
                
        return symbols

    def get_delta(self, node):
        """
        Args:
            node: A node from the standardized tree
            
        Returns:
            Delta: A Delta symbol with its symbols list populated
        """
        delta = Delta(self.j)
        self.j += 1
        delta.symbols = self.get_pre_order_traverse(node)
        return delta

    def get_control(self, ast):
        """
        Create the control list for the CSE Machine from an AST
        
        Args:
            ast: The standardized abstract syntax tree
            
        Returns:
            list: The control list for the CSE Machine
        """
        control = [self.e0, self.get_delta(ast.get_root())]
        return control

    def get_stack(self):
        """
        Create the initial stack for the CSE Machine
        
        Returns:
            list: The initial stack for the CSE Machine
        """
        return [self.e0]

    def get_environment(self):
        """
        Create the initial environment for the CSE Machine
        
        Returns:
            list: The initial environment for the CSE Machine
        """
        return [self.e0]

    def get_cse_machine(self, ast):
        """
        Create a CSE Machine instance from an AST
        
        Args:
            ast: The standardized abstract syntax tree
            
        Returns:
            CSEMachine: A CSE Machine instance ready to execute
        """
        control = self.get_control(ast)
        stack = self.get_stack()
        environment = self.get_environment()
        return CSEMachine(control, stack, environment)
