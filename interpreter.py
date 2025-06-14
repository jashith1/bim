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
            'len': self._builtin_len,
            'upper': self._builtin_upper,
            'lower': self._builtin_lower,
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
    
    def visit_StringNode(self, node):
        """Return the string value"""
        return node.value
    
    def visit_BooleanNode(self, node):
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
        
    def visit_IfNode(self, node):
        """execute if node"""
        condition_value = self.visit(node.condition)
        
        # Convert condition to boolean
        if self.is_truthy(condition_value):
            return self.visit(node.if_body)
        elif node.else_body:
            return self.visit(node.else_body)
        else:
            return None
        
    def visit_BlockNode(self, node):
        """execute contents of block"""
        result = None
        for statement in node.statements:
            result = self.visit(statement)
        return result
    
    def is_truthy(self, value):
        """Determine if a condition is true"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, (int, float)):
            return value != 0
        elif isinstance(value, str):
            return len(value) > 0
        else:
            return value is not None


    def visit_BinaryOpNode(self, node):
        """execute the operation and return its value"""
        left_val = self.visit(node.left)  
        right_val = self.visit(node.right)
        
        # Do the operation
        #math symbols
        if node.operator.type == TokenType.PLUS:
            if isinstance(left_val, str) or isinstance(right_val, str):
                return str(left_val) + str(right_val)
            return left_val + right_val
        
        elif node.operator.type == TokenType.MINUS:
            if isinstance(left_val, str) or isinstance(right_val, str):
                raise Exception("Cannot subtract strings")
            return left_val - right_val
        
        elif node.operator.type == TokenType.MULTIPLY:
            if isinstance(left_val, str) and isinstance(right_val, (int, float)):
                return left_val * int(right_val)
            elif isinstance(left_val, (int, float)) and isinstance(right_val, str):
                return int(left_val) * right_val
            elif isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                return left_val * right_val
            else:
                raise Exception("Unsupported multiplication operation")
            
        elif node.operator.type == TokenType.DIVIDE:
            if isinstance(left_val, str) or isinstance(right_val, str):
                raise Exception("Cannot divide strings")
            if right_val == 0:
                raise Exception("Division by zero!")
            return left_val / right_val
        
        #comparisons
        elif node.operator.type == TokenType.EQUAL:
            return left_val == right_val
        elif node.operator.type == TokenType.NOT_EQUAL:
            return left_val != right_val
        elif node.operator.type == TokenType.LESS_THAN:
            return left_val < right_val
        elif node.operator.type == TokenType.GREATER_THAN:
            return left_val > right_val
        elif node.operator.type == TokenType.LESS_EQUAL:
            return left_val <= right_val
        elif node.operator.type == TokenType.GREATER_EQUAL:
            return left_val >= right_val


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
        if isinstance(args[0], str):
            raise Exception("abs() cannot be applied to strings")
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

    def _builtin_len(self, args):
        """returns length of string"""
        if len(args) != 1:
            raise Exception("len() takes exactly 1 argument")
        if isinstance(args[0], str):
            return len(args[0])
        else:
            raise Exception("len() can only be applied to strings")
    
    def _builtin_upper(self, args):
        """Convert string to uppercase"""
        if len(args) != 1:
            raise Exception("upper() takes exactly 1 argument")
        if isinstance(args[0], str):
            return args[0].upper()
        else:
            raise Exception("upper() can only be applied to strings")
    
    def _builtin_lower(self, args):
        """Convert string to lowercase"""
        if len(args) != 1:
            raise Exception("lower() takes exactly 1 argument")
        if isinstance(args[0], str):
            return args[0].lower()
        else:
            raise Exception("lower() can only be applied to strings")
