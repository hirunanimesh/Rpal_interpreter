from .syntax_parser import NodeType  # Adjust the import path as needed

class StringAst:
    """
    Represents a String Abstract Syntax Tree (AST) node.
    """

    def __init__(self, parser):
        self.parser = parser

    def convert_ast_to_string_ast(self):
        dots = ""
        stack = []

        while self.parser.ast:
            if not stack:
                if self.parser.ast[-1].no_of_children == 0:
                    self.add_strings(dots, self.parser.ast.pop())
                else:
                    node = self.parser.ast.pop()
                    stack.append(node)
            else:
                if self.parser.ast[-1].no_of_children > 0:
                    node = self.parser.ast.pop()
                    stack.append(node)
                    dots += "."
                else:
                    stack.append(self.parser.ast.pop())
                    dots += "."
                    while stack[-1].no_of_children == 0:
                        self.add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]
                        node = stack.pop()
                        node.no_of_children -= 1
                        stack.append(node)

        # Reverse the list
        self.parser.string_ast.reverse()
        return self.parser.string_ast
    
    def add_strings(self, dots, node):
        if node.type in [NodeType.identifier, NodeType.integer, NodeType.string, NodeType.true_value,
                         NodeType.false_value, NodeType.nil, NodeType.dummy]:
            self.parser.string_ast.append(dots + "<" + node.type.name.upper() + ":" + node.value + ">")
        elif node.type == NodeType.fcn_form:
            self.parser.string_ast.append(dots + "function_form")
        else:
            self.parser.string_ast.append(dots + node.value)
