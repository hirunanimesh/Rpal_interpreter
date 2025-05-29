"""
CSE Machine Elements Module for RPAL Interpreter
This module defines the elements used in the CSE Machine.
"""

class Element:
    """Base class for all elements in the CSE Machine."""
    
    def __init__(self, data):
        """
        Initialize a new Element.
        
        Args:
            data (str): The data/value of the element
        """
        self.data = data
    
    def set_data(self, data):
        """Set the data/value of the element."""
        self.data = data
    
    def get_data(self):
        """Get the data/value of the element."""
        return self.data

class Value(Element):
    """Base class for value elements in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new Value element."""
        super().__init__(data)

class Operator(Element):
    """Base class for operator elements in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new Operator element."""
        super().__init__(data)

class ControlStructure(Element):
    """Base class for control structure elements in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new ControlStructure element."""
        super().__init__(data)
        self.symbols = []

class Environment(Element):
    """
    Represents an environment in the CSE Machine.
    
    Attributes:
        index (int): The unique index of the environment
        parent (Environment): The parent environment
        is_removed (bool): Whether the environment has been removed
        values (dict): Dictionary mapping identifiers to values
    """
    
    def __init__(self, index):
        """
        Initialize a new Environment.
        
        Args:
            index (int): The unique index of the environment
        """
        super().__init__("env")
        self.index = index
        self.parent = None
        self.is_removed = False
        self.values = {}
    
    def set_parent(self, parent):
        """Set the parent environment."""
        self.parent = parent
    
    def get_parent(self):
        """Get the parent environment."""
        return self.parent
    
    def set_index(self, index):
        """Set the environment index."""
        self.index = index
    
    def get_index(self):
        """Get the environment index."""
        return self.index
    
    def set_is_removed(self, is_removed):
        """Set whether the environment has been removed."""
        self.is_removed = is_removed
    
    def get_is_removed(self):
        """Get whether the environment has been removed."""
        return self.is_removed
    
    def lookup(self, identifier):
        """
        Look up an identifier in the environment.
        
        Args:
            identifier (Identifier): The identifier to look up
            
        Returns:
            Element: The value associated with the identifier, or the identifier itself if not found
        """
        # Check if the identifier exists in this environment
        for key in self.values:
            if key.get_data() == identifier.get_data():
                return self.values[key]
        
        # If not found, check the parent environment
        if self.parent is not None:
            return self.parent.lookup(identifier)
        
        # If not found anywhere, return the identifier itself
        return Element(identifier.get_data())

class Identifier(Value):
    """Represents an identifier in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new Identifier."""
        super().__init__(data)

class Integer(Value):
    """Represents an integer value in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new Integer."""
        super().__init__(data)

class Text(Value):
    """Represents a text (string) value in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new Text."""
        super().__init__(data)

class Boolean(Value):
    """Represents a boolean value in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new Boolean."""
        super().__init__(data)

class Nil(Value):
    """Represents a nil value in the CSE Machine."""
    
    def __init__(self):
        """Initialize a new Nil."""
        super().__init__("nil")

class Dummy(Value):
    """Represents a dummy value in the CSE Machine."""
    
    def __init__(self):
        """Initialize a new Dummy."""
        super().__init__("dummy")

class Tuple(Value):
    """
    Represents a tuple value in the CSE Machine.
    
    Attributes:
        elements (list): The elements in the tuple
    """
    
    def __init__(self):
        """Initialize a new Tuple."""
        super().__init__("tuple")
        self.elements = []

class UnaryOperator(Operator):
    """Represents a unary operator in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new UnaryOperator."""
        super().__init__(data)

class BinaryOperator(Operator):
    """Represents a binary operator in the CSE Machine."""
    
    def __init__(self, data):
        """Initialize a new BinaryOperator."""
        super().__init__(data)

class Gamma(ControlStructure):
    """Represents a gamma (function application) in the CSE Machine."""
    
    def __init__(self):
        """Initialize a new Gamma."""
        super().__init__("gamma")

class Beta(ControlStructure):
    """Represents a beta (conditional) in the CSE Machine."""
    
    def __init__(self):
        """Initialize a new Beta."""
        super().__init__("beta")

class Delta(ControlStructure):
    """
    Represents a delta (function body) in the CSE Machine.
    
    Attributes:
        index (int): The unique index of the delta
    """
    
    def __init__(self, index):
        """
        Initialize a new Delta.
        
        Args:
            index (int): The unique index of the delta
        """
        super().__init__("delta")
        self.index = index
    
    def set_index(self, index):
        """Set the delta index."""
        self.index = index
    
    def get_index(self):
        """Get the delta index."""
        return self.index

class Lambda(ControlStructure):
    """
    Represents a lambda (function) in the CSE Machine.
    
    Attributes:
        index (int): The unique index of the lambda
        environment (int): The index of the environment where the lambda was created
        identifiers (list): The parameter identifiers
        delta (Delta): The function body
    """
    
    def __init__(self, index):
        """
        Initialize a new Lambda.
        
        Args:
            index (int): The unique index of the lambda
        """
        super().__init__("lambda")
        self.index = index
        self.environment = None
        self.identifiers = []
        self.delta = None
    
    def set_environment(self, environment):
        """Set the environment index."""
        self.environment = environment
    
    def get_environment(self):
        """Get the environment index."""
        return self.environment
    
    def set_delta(self, delta):
        """Set the function body."""
        self.delta = delta
    
    def get_delta(self):
        """Get the function body."""
        return self.delta
    
    def get_index(self):
        """Get the lambda index."""
        return self.index

class Tau(ControlStructure):
    """
    Represents a tau (tuple constructor) in the CSE Machine.
    
    Attributes:
        n (int): The number of elements in the tuple
    """
    
    def __init__(self, n):
        """
        Initialize a new Tau.
        
        Args:
            n (int): The number of elements in the tuple
        """
        super().__init__("tau")
        self.n = n
    
    def set_n(self, n):
        """Set the number of elements."""
        self.n = n
    
    def get_n(self):
        """Get the number of elements."""
        return self.n

class Ystar(ControlStructure):
    """Represents a Y* (fixed-point combinator) in the CSE Machine."""
    
    def __init__(self):
        """Initialize a new Ystar."""
        super().__init__("<Y*>")

class Eta(ControlStructure):
    """
    Represents an eta (recursive function wrapper) in the CSE Machine.
    
    Attributes:
        index (int): The unique index of the eta
        environment (int): The index of the environment where the eta was created
        identifier (Identifier): The function identifier
        lambda_func (Lambda): The wrapped lambda function
    """
    
    def __init__(self):
        """Initialize a new Eta."""
        super().__init__("eta")
        self.index = None
        self.environment = None
        self.identifier = None
        self.lambda_func = None
    
    def set_index(self, index):
        """Set the eta index."""
        self.index = index
    
    def get_index(self):
        """Get the eta index."""
        return self.index
    
    def set_environment(self, environment):
        """Set the environment index."""
        self.environment = environment
    
    def get_environment(self):
        """Get the environment index."""
        return self.environment
    
    def set_identifier(self, identifier):
        """Set the function identifier."""
        self.identifier = identifier
    
    def set_lambda(self, lambda_func):
        """Set the wrapped lambda function."""
        self.lambda_func = lambda_func
    
    def get_lambda(self):
        """Get the wrapped lambda function."""
        return self.lambda_func

class Error(Element):
    """Represents an error in the CSE Machine."""
    
    def __init__(self):
        """Initialize a new Error."""
        super().__init__("error")
