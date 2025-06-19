from bim_token import TokenType
from exceptions import *

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
            'range': self._builtin_range,
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
        
        for elif_condition, elif_body in node.elif_clauses:
            elif_condition_value = self.visit(elif_condition)
            if self.is_truthy(elif_condition_value):
                return self.visit(elif_body)

        if node.else_body:
            return self.visit(node.else_body)
        
        return None
        
    def visit_BlockNode(self, node):
        """Execute block with break/continue propagation"""
        result = None
        for statement in node.statements:
            try:
                result = self.visit(statement)
            except (BreakException, ContinueException):
                # raise break/continue so that the loop handler can catch it
                raise
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
    
    def visit_WhileNode(self, node):
        """Execute while loop with break/continue support"""
        result = None
        try:
            while True:
                condition_value = self.visit(node.condition)
                if not self.is_truthy(condition_value):
                    break
                
                try:
                    result = self.visit(node.body)
                except ContinueException:
                    continue
                except BreakException:
                    break
                    
        except BreakException:
            pass
        
        return result


    def visit_ForNode(self, node):
        """Execute for loop with break/continue support"""
        result = None
        
        iterable_value = self.visit(node.iterable)
        
        # Handle different types of iterables
        if isinstance(iterable_value, list):
            items = iterable_value
        elif isinstance(iterable_value, str):
            items = list(iterable_value)
        elif isinstance(iterable_value, range):
            items = list(iterable_value)
        else:
            raise Exception(f"Cannot iterate over {type(iterable_value)}")
        
        # Save the old value of the loop variable
        old_value = self.variables.get(node.variable)
        
        try:
            for item in items:
                self.variables[node.variable] = item
                
                try:
                    result = self.visit(node.body)
                except ContinueException:
                    continue
                except BreakException:
                    break
                    
        except BreakException:
            pass
        finally:
            # Restore the old value of the loop variable
            if old_value is not None:
                self.variables[node.variable] = old_value
            elif node.variable in self.variables:
                del self.variables[node.variable]
        
        return result

    
    def visit_BreakNode(self, node):
        """Handle break statement by raising an exception"""
        raise BreakException()

    def visit_ContinueNode(self, node):
        """Handle continue statement by raising an exception"""
        raise ContinueException()


    def visit_RangeNode(self, node):
        """Create a range object"""
        start_val = self.visit(node.start)
        stop_val = self.visit(node.stop)
        
        if node.step:
            step_val = self.visit(node.step)
            return range(int(start_val), int(stop_val), int(step_val))
        else:
            return range(int(start_val), int(stop_val))

    def visit_FunctionCallNode(self, node):
        """execute the function call with given args"""
        function_name = node.function_name
        
        if function_name in self.builtin_functions:
            arg_values = [self.visit(arg) for arg in node.arguments]
            return self.builtin_functions[function_name](arg_values)
        else:
            raise Exception(f"Unknown function: {function_name}")
        
    def visit_ArrayNode(self, node):
        """Create an array"""
        elements = []
        for element_expr in node.elements:
            elements.append(self.visit(element_expr))
        return elements

    def visit_IndexNode(self, node):
        """Get element from array by index"""
        array_value = self.visit(node.array)
        index_value = self.visit(node.index)
        
        if not isinstance(array_value, (list, str)):
            raise Exception(f"Cannot index {type(array_value).__name__}")
        
        if not isinstance(index_value, (int, float)):
            raise Exception("Array index must be a number")
        
        index = int(index_value)
        
        try:
            return array_value[index]
        except IndexError:
            raise Exception(f"Array index {index} out of range")

    def visit_IndexAssignmentNode(self, node):
        """Assign value to array element"""
        array_value = self.visit(node.array)
        index_value = self.visit(node.index)
        new_value = self.visit(node.value)
        
        if not isinstance(array_value, list):
            raise Exception(f"Cannot assign to index of {type(array_value).__name__}")
        
        if not isinstance(index_value, (int, float)):
            raise Exception("Array index must be a number")
        
        index = int(index_value)
        
        try:
            array_value[index] = new_value
            return new_value
        except IndexError:
            raise Exception(f"Array index {index} out of range")

    def visit_MethodCallNode(self, node):
        """Handle method calls on objects"""
        object_value = self.visit(node.object_expr)
        method_name = node.method_name
        arg_values = [self.visit(arg) for arg in node.arguments]
        
        if isinstance(object_value, list):
            return self._handle_array_method(object_value, method_name, arg_values)
        elif isinstance(object_value, str):
            return self._handle_string_method(object_value, method_name, arg_values)
        else:
            raise Exception(f"Object of type {type(object_value).__name__} has no methods")


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

    def _builtin_range(self, args):
        """Range function - creates a range object"""
        if len(args) == 1:
            return range(int(args[0]))
        elif len(args) == 2:
            return range(int(args[0]), int(args[1]))
        elif len(args) == 3:
            return range(int(args[0]), int(args[1]), int(args[2]))
        else:
            raise Exception("range() takes 1 to 3 arguments")
        
    def _handle_array_method(self, array, method_name, args):
        """Handle array methods"""
        if method_name == "push":
            for arg in args:
                array.append(arg)
            return len(array)
        
        elif method_name == "pop":
            if len(args) != 0:
                raise Exception("pop() takes no arguments")
            if len(array) == 0:
                raise Exception("Cannot pop from empty array")
            return array.pop()
        
        elif method_name == "length":
            if len(args) != 0:
                raise Exception("length takes no arguments")
            return len(array)
        
        elif method_name == "insert":
            # Insert element at specific index
            if len(args) != 2:
                raise Exception("insert() takes exactly 2 arguments (index, value)")
            index, value = args
            if not isinstance(index, (int, float)):
                raise Exception("Insert index must be a number")
            array.insert(int(index), value)
            return None
        
        elif method_name == "remove":
            # Remove element at specific index
            if len(args) != 1:
                raise Exception("remove() takes exactly 1 argument (index)")
            index = args[0]
            if not isinstance(index, (int, float)):
                raise Exception("Remove index must be a number")
            try:
                return array.pop(int(index))
            except IndexError:
                raise Exception(f"Array index {int(index)} out of range")
        
        else:
            raise Exception(f"Array has no method '{method_name}'")

    def _handle_string_method(self, string, method_name, args):
        """Handle string methods"""
        if method_name == "length":
            if len(args) != 0:
                raise Exception("length takes no arguments")
            return len(string)
        
        elif method_name == "charAt":
            if len(args) != 1:
                raise Exception("charAt() takes exactly 1 argument")
            index = args[0]
            if not isinstance(index, (int, float)):
                raise Exception("charAt index must be a number")
            try:
                return string[int(index)]
            except IndexError:
                raise Exception(f"String index {int(index)} out of range")
                
        else:
            # Fall back to existing string methods
            if method_name == "upper":
                return string.upper()
            elif method_name == "lower":
                return string.lower()
            else:
                raise Exception(f"String has no method '{method_name}'")
