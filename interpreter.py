from bim_token import TokenType

#executes the created AST
class Interpreter:
    def __init__(self):
        #stored variables
        self.variables = {} 
        self.builtin_functions = {
            'print': self._builtin_print,
            'abs': self._builtin_abs,
            'min': self._builtin_min,
            'max': self._builtin_max,
        }

    def visit(self, node):
        """execute a node and return it"""
        if isinstance(node, (int, float)):
            return node

        method_name = f'visit_{type(node).__name__}'
        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)
        else:
            raise Exception(f"No visit method for {type(node).__name__}")
    
    def visit_NumberNode(self, node):
        """just return the number"""
        return node.value
    
    def visit_UnaryOpNode(self, node):
        """return the value of number along with its sign"""
        operand_val = self.visit(node.operand)
        
        if node.operator.type == TokenType.PLUS:
            return +operand_val
        elif node.operator.type == TokenType.MINUS:
            return -operand_val
    
    def visit_VariableNode(self, node):
        """Look up a variable's value"""
        if node.name in self.variables:
            return self.variables[node.name]
        else:
            raise Exception(f"Undefined variable: {node.name}")

    def visit_BinaryOpNode(self, node):
        """execute the operation and return its value"""
        left_val = self.visit(node.left)  
        right_val = self.visit(node.right)
        
        # Do the operation
        if node.operator.type == TokenType.PLUS:
            return left_val + right_val
        elif node.operator.type == TokenType.MINUS:
            return left_val - right_val
        elif node.operator.type == TokenType.MULTIPLY:
            return left_val * right_val
        elif node.operator.type == TokenType.DIVIDE:
            if right_val == 0:
                raise Exception("Division by zero!")
            return left_val / right_val

    def visit_AssignmentNode(self, node):
        """Store the assigned variable"""
        value = self.visit(node.value) 
        self.variables[node.variable_name] = value
        return value 

    def visit_FunctionCallNode(self, node):
        """execute the function call with given args"""
        function_name = node.function_name
        
        if function_name in self.builtin_functions:
            arg_values = [self.visit(arg) for arg in node.arguments]
            return self.builtin_functions[function_name](arg_values)
        else:
            raise Exception(f"Unknown function: {function_name}")

    def _builtin_print(self, args):
        """prints all arguments separated by spaces"""
        print(' '.join(str(arg) for arg in args))

    def _builtin_abs(self, args):
        """Absolute value function"""
        if len(args) != 1:
            raise Exception("abs() takes exactly 1 argument")
        return abs(args[0])
    
    def _builtin_min(self, args):
        """Minimum function"""
        if len(args) == 0:
            raise Exception("min() takes at least 1 argument")
        return min(args)
    
    def _builtin_max(self, args):
        """Maximum function"""
        if len(args) == 0:
            raise Exception("max() takes at least 1 argument")
        return max(args)
