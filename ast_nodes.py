class ASTNode:
    """Base class for all AST nodes"""
    pass

class NumberNode(ASTNode):
    """Represents numbers (including decimals)"""
    def __init__(self, value):
        self.value = float(value)
    
    def __repr__(self):
        return f"NumberNode({self.value})"
    
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
