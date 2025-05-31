
from .symbols import *

class CSEMachine:
    """
    CSE Machine for evaluating standardized RPAL programs
    """
    def __init__(self, control, stack, environment):
        """
        Initialize a new CSE Machine instance
        
        Args:
            control (list): The control list of symbols to process
            stack (list): The stack for storing intermediate results
            environment (list): The environment list for variable bindings
        """
        self.control = control
        self.stack = stack
        self.environment = environment

    def execute(self):
        
        current_environment = self.environment[0]
        j = 1
        while self.control:
            
            
            current_symbol = self.control.pop()
            
            if isinstance(current_symbol, Id):
                # Handle identifier lookup in the environment
                self.stack.insert(0, current_environment.lookup(current_symbol))
                
            elif isinstance(current_symbol, Lambda):
                # Handle lambda expression
                current_symbol.set_environment(current_environment.get_index())
                self.stack.insert(0, current_symbol)
                
            elif isinstance(current_symbol, Gamma):
                # Handle function application
                next_symbol = self.stack.pop(0)
                
                if isinstance(next_symbol, Lambda):
                    # Handle Lambda application
                    lambda_expr = next_symbol
                    e = E(j)
                    j += 1
                    
                    if len(lambda_expr.identifiers) == 1:
                        # Single parameter
                        temp = self.stack.pop(0)
                        e.values[lambda_expr.identifiers[0]] = temp
                    else:
                        # Multiple parameters as tuple
                        tup = self.stack.pop(0)
                        for i, id in enumerate(lambda_expr.identifiers):
                            e.values[id] = tup.symbols[i]
                    
                    # Set up environment chain
                    for env in self.environment:
                        if env.get_index() == lambda_expr.get_environment():
                            e.set_parent(env)
                    
                    current_environment = e
                    self.control.append(e)
                    self.control.append(lambda_expr.get_delta())
                    self.stack.insert(0, e)
                    self.environment.append(e)
                    
                elif isinstance(next_symbol, Tup):
                    # Handle tuple indexing
                    tup = next_symbol
                    i = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, tup.symbols[i - 1])
                    
                elif isinstance(next_symbol, Ystar):
                    # Handle recursion with Y* operator
                    lambda_expr = self.stack.pop(0)
                    eta = Eta()
                    eta.set_index(lambda_expr.get_index())
                    eta.set_environment(lambda_expr.get_environment())
                    eta.set_identifier(lambda_expr.identifiers[0])
                    eta.set_lambda(lambda_expr)
                    self.stack.insert(0, eta)
                    
                elif isinstance(next_symbol, Eta):
                    # Handle Eta expression for recursion
                    eta = next_symbol
                    lambda_expr = eta.get_lambda()
                    self.control.append(Gamma())
                    self.control.append(Gamma())
                    self.stack.insert(0, eta)
                    self.stack.insert(0, lambda_expr)
                    
                else:
                    # Handle built-in functions
                    if next_symbol.get_data() == "Print":
                        # Print function - prints the value
                        value = self.stack.pop(0)
                        value.get_data()              ###########################
                        self.stack.insert(0, value)
                        
                    elif next_symbol.get_data() == "Stem":
                        # Stem function - gets first character of string
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[0])
                        self.stack.insert(0, s)
                        
                    elif next_symbol.get_data() == "Stern":
                        # Stern function - gets all but first character of string
                        s = self.stack.pop(0)
                        s.set_data(s.get_data()[1:])
                        self.stack.insert(0, s)
                        
                    elif next_symbol.get_data() == "Conc":
                        # Conc function - concatenates two strings
                        s1 = self.stack.pop(0)
                        s2 = self.stack.pop(0)
                        s1.set_data(s1.get_data() + s2.get_data())
                        self.stack.insert(0, s1)
                        
                    elif next_symbol.get_data() == "Order":
                        # Order function - gets length of tuple
                        tup = self.stack.pop(0)
                        n = Int(str(len(tup.symbols)))
                        self.stack.insert(0, n)
                        
                    elif next_symbol.get_data() == "Isinteger":
                        # Isinteger function - checks if value is integer
                        if isinstance(self.stack[0], Int):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Null":
                        # Null function - checks if tuple is empty
                        tup = self.stack.pop(0)
                        if len(tup.symbols) == 0:
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                            
                    elif next_symbol.get_data() == "Itos":
                        # Itos function - converts integer to string
                        i = self.stack.pop(0)
                        self.stack.insert(0, Str(i.get_data()))
                        
                    elif next_symbol.get_data() == "Isstring":
                        # Isstring function - checks if value is string
                        if isinstance(self.stack[0], Str):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Istuple":
                        # Istuple function - checks if value is tuple
                        if isinstance(self.stack[0], Tup):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Isdummy":
                        # Isdummy function - checks if value is dummy
                        if isinstance(self.stack[0], Dummy):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Istruthvalue":
                        # Istruthvalue function - checks if value is boolean
                        if isinstance(self.stack[0], Bool):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
                    elif next_symbol.get_data() == "Isfunction":
                        # Isfunction function - checks if value is function
                        if isinstance(self.stack[0], Lambda):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                        
            elif isinstance(current_symbol, E):
                # Handle environment cleanup
                self.stack.pop(1)
                self.environment[current_symbol.get_index()].set_is_removed(True)
                y = len(self.environment)
                while y > 0:
                    if not self.environment[y - 1].get_is_removed():
                        current_environment = self.environment[y - 1]
                        break
                    else:
                        y -= 1
                        
            elif isinstance(current_symbol, Rator):
                if isinstance(current_symbol, Uop):
                    # Handle unary operations
                    rator = current_symbol
                    rand = self.stack.pop(0)
                    self.stack.insert(0, self.apply_unary_operation(rator, rand))
                    
                if isinstance(current_symbol, Bop):
                    # Handle binary operations
                    rator = current_symbol
                    rand1 = self.stack.pop(0)
                    rand2 = self.stack.pop(0)
                    self.stack.insert(0, self.apply_binary_operation(rator, rand1, rand2))
                    
            elif isinstance(current_symbol, Beta):
                # Handle conditional branching
                if self.stack[0].get_data() == "true":
                    self.control.pop()
                else:
                    self.control.pop(-2)
                self.stack.pop(0)
                
            elif isinstance(current_symbol, Tau):
                # Handle tuple creation
                tau = current_symbol
                tup = Tup()
                for _ in range(tau.get_n()):
                    tup.symbols.append(self.stack.pop(0))
                self.stack.insert(0, tup)
                
            elif isinstance(current_symbol, Delta):
                # Handle code block execution
                self.control.extend(current_symbol.symbols)
                
            elif isinstance(current_symbol, B):
                # Handle conditional code block
                self.control.extend(current_symbol.symbols)
                
            else:
                # Handle other symbols (literals)
                self.stack.insert(0, current_symbol)

    def convert_string_to_bool(self, data):
        """
        Convert string representation of boolean to Python boolean
        
        Args:
            data (str): String representation of boolean ("true" or "false")
            
        """
        if data == "true":
            return True
        elif data == "false":
            return False

    def apply_unary_operation(self, rator, rand):
        """
        Args:
            rator (Uop): Unary operator
            rand (Rand): Operand
            
        Returns:
            Symbol: Result of the operation
        """
        if rator.get_data() == "neg":
            val = int(rand.get_data())
            return Int(str(-1 * val))
        elif rator.get_data() == "not":
            val = self.convert_string_to_bool(rand.get_data())
            return Bool(str(not val).lower())
        else:
            return Err()

    def apply_binary_operation(self, rator, rand1, rand2):
        """      
        Args:
            rator (Bop): Binary operator
            rand1 (Rand): First operand
            rand2 (Rand): Second operand
            
        Returns:
            Symbol: Result of the operation
        """
        if rator.get_data() == "+":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 + val2))
        elif rator.data == "-":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 - val2))
        elif rator.data == "*":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 * val2))
        elif rator.data == "/":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(int(val1 / val2)))
        elif rator.data == "**":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 ** val2))
        elif rator.data == "&":
            val1 = self.convert_string_to_bool(rand1.data)
            val2 = self.convert_string_to_bool(rand2.data)
            return Bool(str(val1 and val2).lower())
        elif rator.data == "or":
            val1 = self.convert_string_to_bool(rand1.data)
            val2 = self.convert_string_to_bool(rand2.data)
            return Bool(str(val1 or val2).lower())
        elif rator.data == "eq":
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 == val2).lower())
        elif rator.data == "ne":
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 != val2).lower())
        elif rator.data == "ls":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 < val2).lower())
        elif rator.data == "le":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 <= val2).lower())
        elif rator.data == "gr":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 > val2).lower())
        elif rator.data == "ge":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 >= val2).lower())
        elif rator.data == "aug":
            if isinstance(rand2, Tup):
                rand1.symbols.extend(rand2.symbols)
            else:
                rand1.symbols.append(rand2)
            return rand1
        else:
            return Err()

    def get_tuple_value(self, tup):
        """
        Get string representation of a tuple
        
        Args:
            tup (Tup): Tuple to convert to string
            
        Returns:
            str: String representation of the tuple
        """
        temp = "("
        for symbol in tup.symbols:
            if isinstance(symbol, Tup):
                temp += self.get_tuple_value(symbol) + ", "
            else:
                temp += symbol.get_data() + ", "
        temp = temp[:-2] + ")" if len(tup.symbols) > 0 else temp + ")"
        return temp

    def get_answer(self):
        """
        Execute the CSE Machine and get the final result
        
        Returns:
            str: String representation of the final result
        """
        self.execute()
        if isinstance(self.stack[0], Tup):
            return self.get_tuple_value(self.stack[0])
        return self.stack[0].get_data()
