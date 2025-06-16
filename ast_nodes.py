class ASTNode:
    """Base class for all AST nodes"""
    pass

class NumberNode(ASTNode):
    """Represents numbers (including decimals)"""
    def __init__(self, value):
        self.value = float(value)
    
    def __repr__(self):
        return f"NumberNode({self.value})"
    
class StringNode(ASTNode):
    def __init__(self, value):
        self.value = str(value)
    
    def __repr__(self):
        return f"StringNode('{self.value}')"
    
class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = bool(value)
    
    def __repr__(self):
        return f"BooleanNode({self.value})"
    
class UnaryOpNode(ASTNode):
    """Represents the +/- in front of number to signify signs"""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOpNode({self.operator.type}, {self.operand})"

class BinaryOpNode(ASTNode):
    """Represents an operations (ex: 3+4 or 10-6)"""
    def __init__(self, left, operator, right):
        self.left = left      # Left side (type is another AST node)
        self.operator = operator  # The operator (+, -, etc)
        self.right = right    # Right side (type is another AST node)
    
    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.operator.type}, {self.right})"

class VariableNode(ASTNode):
    """Represents variable names"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"VariableNode({self.name})"

class AssignmentNode(ASTNode):
    """Represents variables"""
    def __init__(self, variable_name, value):
        self.variable_name = variable_name
        self.value = value
    
    def __repr__(self):
        return f"AssignmentNode({self.variable_name} = {self.value})"

class FunctionCallNode(ASTNode):
    """Represents function calls (like print())"""
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments
    
    def __repr__(self):
        return f"FunctionCallNode({self.function_name}, {self.arguments})"

class IfNode(ASTNode):
    """Represents if statements"""
    def __init__(self, condition, if_body, elif_clauses = None, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
        self.elif_clauses = elif_clauses or []
    
    def __repr__(self):
        result = f"IfNode(condition={self.condition}, if_body={self.if_body}"
        if self.elif_clauses:
            result += f", elif_clauses={self.elif_clauses}"
        if self.else_body:
            result += f", else_body={self.else_body}"
        result += ")"
        return result

class BlockNode(ASTNode):
    """Represents statement blocks"""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"BlockNode({self.statements})"

