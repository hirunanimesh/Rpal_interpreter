"""
CSE Machine Engine Module for RPAL Interpreter
This module implements the CSE Machine execution engine.
"""

from CSEMachine.elements import *

class CSEEngine:
    """
    CSE Machine execution engine for RPAL programs.
    
    Attributes:
        control (list): The control structure (sequence of operations)
        stack (list): The execution stack
        environment (list): The environment stack
    """
    
    def __init__(self, control, stack, environment):
        """
        Initialize a new CSEEngine.
        
        Args:
            control (list): The control structure
            stack (list): The execution stack
            environment (list): The environment stack
        """
        self.control = control
        self.stack = stack
        self.environment = environment
    
    def evaluate(self):
        """
        Execute the CSE Machine and return the result.
        
        Returns:
            str: The result of executing the program
        """
        # Set up the initial environment
        current_environment = self.environment[0]
        env_counter = 1
        
        # Execute until the control structure is empty
        while self.control:
            # Get the next element from the control structure
            current_element = self.control.pop(0)
            
            # Process the element based on its type
            if isinstance(current_element, Identifier):
                # Look up the identifier in the current environment
                value = current_environment.lookup(current_element)
                self.stack.insert(0, value)
            
            elif isinstance(current_element, Lambda):
                # Set the environment for the lambda
                current_element.set_environment(current_environment.get_index())
                self.stack.insert(0, current_element)
            
            elif isinstance(current_element, Gamma):
                # Function application
                next_element = self.stack.pop(0)
                
                if isinstance(next_element, Lambda):
                    # Handle lambda application
                    lambda_expr = next_element
                    
                    # Create a new environment
                    new_env = Environment(env_counter)
                    env_counter += 1
                    
                    # Bind parameters
                    if len(lambda_expr.identifiers) == 1:
                        # Single parameter
                        param_value = self.stack.pop(0)
                        new_env.values[lambda_expr.identifiers[0]] = param_value
                    else:
                        # Multiple parameters (tuple)
                        tuple_value = self.stack.pop(0)
                        for i, identifier in enumerate(lambda_expr.identifiers):
                            new_env.values[identifier] = tuple_value.elements[i]
                    
                    # Set up environment chain
                    for env in self.environment:
                        if env.get_index() == lambda_expr.get_environment():
                            new_env.set_parent(env)
                            break
                    
                    # Update current environment
                    current_environment = new_env
                    
                    # Add environment marker to control
                    self.control.insert(0, new_env)
                    
                    # Add function body to control
                    self.control = lambda_expr.get_delta().symbols + self.control
                    
                    # Add environment to stack and environment list
                    self.stack.insert(0, new_env)
                    self.environment.append(new_env)
                
                elif isinstance(next_element, Tuple):
                    # Handle tuple selection
                    tuple_value = next_element
                    index = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, tuple_value.elements[index - 1])
                
                elif isinstance(next_element, Ystar):
                    # Handle Y* (fixed-point combinator)
                    lambda_expr = self.stack.pop(0)
                    eta = Eta()
                    eta.set_index(lambda_expr.get_index())
                    eta.set_environment(lambda_expr.get_environment())
                    eta.set_identifier(lambda_expr.identifiers[0])
                    eta.set_lambda(lambda_expr)
                    self.stack.insert(0, eta)
                
                elif isinstance(next_element, Eta):
                    # Handle Eta (recursive function wrapper)
                    eta = next_element
                    lambda_expr = eta.get_lambda()
                    
                    # Set up recursive application
                    self.control.insert(0, Gamma())
                    self.control.insert(0, Gamma())
                    self.stack.insert(0, eta)
                    self.stack.insert(0, lambda_expr)
                
                else:
                    # Handle built-in functions
                    if next_element.get_data() == "Print":
                        # Print function (no-op in this implementation)
                        pass
                    
                    elif next_element.get_data() == "Stem":
                        # Stem function (first character of string)
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[0])
                        self.stack.insert(0, s)
                    
                    elif next_element.get_data() == "Stern":
                        # Stern function (all but first character of string)
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[1:])
                        self.stack.insert(0, s)
                    
                    elif next_element.get_data() == "Conc":
                        # Concatenation function
                        s1 = self.stack.pop(0)
                        s2 = self.stack.pop(0)
                        s1.set_data(s1.get_data() + s2.get_data())
                        self.stack.insert(0, s1)
                    
                    elif next_element.get_data() == "Order":
                        # Order function (tuple length)
                        tuple_value = self.stack.pop(0)
                        n = Integer(str(len(tuple_value.elements)))
                        self.stack.insert(0, n)
                    
                    elif next_element.get_data() == "Isinteger":
                        # Isinteger function
                        if isinstance(self.stack[0], Integer):
                            self.stack.insert(0, Boolean("true"))
                        else:
                            self.stack.insert(0, Boolean("false"))
                        self.stack.pop(1)
                    
                    elif next_element.get_data() == "Isstring":
                        # Isstring function
                        if isinstance(self.stack[0], Text):
                            self.stack.insert(0, Boolean("true"))
                        else:
                            self.stack.insert(0, Boolean("false"))
                        self.stack.pop(1)
                    
                    elif next_element.get_data() == "Istuple":
                        # Istuple function
                        if isinstance(self.stack[0], Tuple):
                            self.stack.insert(0, Boolean("true"))
                        else:
                            self.stack.insert(0, Boolean("false"))
                        self.stack.pop(1)
                    
                    elif next_element.get_data() == "Isdummy":
                        # Isdummy function
                        if isinstance(self.stack[0], Dummy):
                            self.stack.insert(0, Boolean("true"))
                        else:
                            self.stack.insert(0, Boolean("false"))
                        self.stack.pop(1)
                    
                    elif next_element.get_data() == "Istruthvalue":
                        # Istruthvalue function
                        if isinstance(self.stack[0], Boolean):
                            self.stack.insert(0, Boolean("true"))
                        else:
                            self.stack.insert(0, Boolean("false"))
                        self.stack.pop(1)
                    
                    elif next_element.get_data() == "Isfunction":
                        # Isfunction function
                        if isinstance(self.stack[0], Lambda):
                            self.stack.insert(0, Boolean("true"))
                        else:
                            self.stack.insert(0, Boolean("false"))
                        self.stack.pop(1)
            
            elif isinstance(current_element, Environment):
                # Environment marker - pop the environment
                self.stack.pop(1)  # Remove the environment from the stack
                self.environment[current_element.get_index()].set_is_removed(True)
                
                # Find the next active environment
                for i in range(len(self.environment) - 1, -1, -1):
                    if not self.environment[i].get_is_removed():
                        current_environment = self.environment[i]
                        break
            
            elif isinstance(current_element, UnaryOperator):
                # Handle unary operators
                operand = self.stack.pop(0)
                self.stack.insert(0, self._apply_unary_operation(current_element, operand))
            
            elif isinstance(current_element, BinaryOperator):
                # Handle binary operators
                right_operand = self.stack.pop(0)
                left_operand = self.stack.pop(0)
                self.stack.insert(0, self._apply_binary_operation(current_element, left_operand, right_operand))
            
            elif isinstance(current_element, Beta):
                # Handle conditional (beta)
                condition = self.stack.pop(0)
                
                if condition.get_data() == "true":
                    # Execute the true branch
                    self.control = current_element.symbols[0].symbols + self.control
                else:
                    # Execute the false branch
                    self.control = current_element.symbols[1].symbols + self.control
            
            elif isinstance(current_element, Tau):
                # Handle tuple construction (tau)
                tuple_value = Tuple()
                
                # Pop n elements from the stack and add them to the tuple
                for _ in range(current_element.get_n()):
                    tuple_value.elements.insert(0, self.stack.pop(0))
                
                self.stack.insert(0, tuple_value)
            
            elif isinstance(current_element, Delta):
                # Handle delta (function body)
                # Add all symbols to the control structure
                self.control = current_element.symbols + self.control
            
            else:
                # Handle other elements (values)
                self.stack.insert(0, current_element)
        
        # Return the final result
        return self._format_result(self.stack[0])
    
    def _convert_string_to_bool(self, data):
        """
        Convert a string representation of a boolean to a Python boolean.
        
        Args:
            data (str): The string representation
            
        Returns:
            bool: The corresponding Python boolean
        """
        if data == "true":
            return True
        elif data == "false":
            return False
        return None
    
    def _apply_unary_operation(self, operator, operand):
        """
        Apply a unary operation to an operand.
        
        Args:
            operator (UnaryOperator): The operator to apply
            operand (Element): The operand
            
        Returns:
            Element: The result of the operation
        """
        if operator.get_data() == "neg":
            # Negation
            value = int(operand.get_data())
            return Integer(str(-value))
        
        elif operator.get_data() == "not":
            # Logical NOT
            value = self._convert_string_to_bool(operand.get_data())
            return Boolean(str(not value).lower())
        
        # Unknown operator
        return Error()
    
    def _apply_binary_operation(self, operator, left_operand, right_operand):
        """
        Apply a binary operation to two operands.
        
        Args:
            operator (BinaryOperator): The operator to apply
            left_operand (Element): The left operand
            right_operand (Element): The right operand
            
        Returns:
            Element: The result of the operation
        """
        op = operator.get_data()
        
        # For comparison operators, we need to handle different types
        if op in ["ls", "le", "gr", "ge"]:
            # Try numeric comparison first
            try:
                left_value = int(left_operand.get_data())
                right_value = int(right_operand.get_data())
                
                if op == "ls":
                    return Boolean(str(left_value < right_value).lower())
                elif op == "le":
                    return Boolean(str(left_value <= right_value).lower())
                elif op == "gr":
                    return Boolean(str(left_value > right_value).lower())
                elif op == "ge":
                    return Boolean(str(left_value >= right_value).lower())
            except (ValueError, TypeError):
                # Fall back to string comparison
                left_value = str(left_operand.get_data())
                right_value = str(right_operand.get_data())
                
                if op == "ls":
                    return Boolean(str(left_value < right_value).lower())
                elif op == "le":
                    return Boolean(str(left_value <= right_value).lower())
                elif op == "gr":
                    return Boolean(str(left_value > right_value).lower())
                elif op == "ge":
                    return Boolean(str(left_value >= right_value).lower())
        
        # For arithmetic operators, we need to ensure numeric operands
        elif op in ["+", "-", "*", "/", "**"]:
            # Addition can work with strings or numbers
            if op == "+":
                # Try numeric addition first
                try:
                    left_value = int(left_operand.get_data())
                    right_value = int(right_operand.get_data())
                    return Integer(str(left_value + right_value))
                except (ValueError, TypeError):
                    # Fall back to string concatenation
                    return Text(str(left_operand.get_data()) + str(right_operand.get_data()))
            
            # Other arithmetic operators require numeric operands
            else:
                try:
                    left_value = int(left_operand.get_data())
                    right_value = int(right_operand.get_data())
                    
                    if op == "-":
                        return Integer(str(left_value - right_value))
                    elif op == "*":
                        return Integer(str(left_value * right_value))
                    elif op == "/":
                        return Integer(str(int(left_value / right_value)))
                    elif op == "**":
                        return Integer(str(left_value ** right_value))
                except (ValueError, TypeError):
                    # Provide a more helpful error message
                    return Error(f"Cannot apply '{op}' to non-numeric values: {left_operand.get_data()} and {right_operand.get_data()}")
        
        elif op == "&":
            # Logical AND
            left_value = self._convert_string_to_bool(left_operand.get_data())
            right_value = self._convert_string_to_bool(right_operand.get_data())
            return Boolean(str(left_value and right_value).lower())
        
        elif op == "or":
            # Logical OR
            left_value = self._convert_string_to_bool(left_operand.get_data())
            right_value = self._convert_string_to_bool(right_operand.get_data())
            return Boolean(str(left_value or right_value).lower())
        
        elif op == "eq":
            # Equality
            left_value = left_operand.get_data()
            right_value = right_operand.get_data()
            return Boolean(str(left_value == right_value).lower())
        
        elif op == "ne":
            # Inequality
            left_value = left_operand.get_data()
            right_value = right_operand.get_data()
            return Boolean(str(left_value != right_value).lower())
        
        elif op == "ls":
            # Less than
            left_value = int(left_operand.get_data())
            right_value = int(right_operand.get_data())
            return Boolean(str(left_value < right_value).lower())
        
        elif op == "le":
            # Less than or equal
            left_value = int(left_operand.get_data())
            right_value = int(right_operand.get_data())
            return Boolean(str(left_value <= right_value).lower())
        
        elif op == "gr":
            # Greater than
            left_value = int(left_operand.get_data())
            right_value = int(right_operand.get_data())
            return Boolean(str(left_value > right_value).lower())
        
        elif op == "ge":
            # Greater than or equal
            left_value = int(left_operand.get_data())
            right_value = int(right_operand.get_data())
            return Boolean(str(left_value >= right_value).lower())
        
        elif op == "aug":
            # Augmentation (tuple concatenation)
            if isinstance(right_operand, Tuple):
                left_operand.elements.extend(right_operand.elements)
            else:
                left_operand.elements.append(right_operand)
            return left_operand
        
        # Unknown operator
        return Error()
    
    def _format_tuple(self, tuple_value):
        """
        Format a tuple value as a string.
        
        Args:
            tuple_value (Tuple): The tuple to format
            
        Returns:
            str: The formatted tuple string
        """
        elements = []
        
        for element in tuple_value.elements:
            if isinstance(element, Tuple):
                elements.append(self._format_tuple(element))
            else:
                elements.append(element.get_data())
        
        return "(" + ", ".join(elements) + ")"
    
    def _format_result(self, result):
        """
        Format the final result as a string.
        
        Args:
            result (Element): The result element
            
        Returns:
            str: The formatted result string
        """
        if isinstance(result, Tuple):
            return self._format_tuple(result)
        
        return result.get_data()
