class ASTNode:
    """Base class for all AST nodes"""
    pass

class NumberNode(ASTNode):
    """Represents numbers (including decimals)"""
    def __init__(self, value):
        self.value = float(value)
    
    def __repr__(self):
        return f"NumberNode({self.value})"

class BinaryOpNode(ASTNode):
    """Represents an operations (ex: 3+4 or 10-6)"""
    def __init__(self, left, operator, right):
        self.left = left      # Left side (type is another AST node)
        self.operator = operator  # The operator (+, -, etc)
        self.right = right    # Right side (type is another AST node)
    
    def __repr__(self):
        return f"BinaryOpNode({self.left}, {self.operator.type}, {self.right})"

