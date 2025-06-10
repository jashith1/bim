from bim_token import TokenType

#executes the created AST
class Interpreter:
    def visit(self, node):
        """execute a node and return it"""
        method_name = f'visit_{type(node).__name__}'
        
        if hasattr(self, method_name):
            visitor = getattr(self, method_name)
            return visitor(node)
        else:
            raise Exception(f"No visit method for {type(node).__name__}")
    
    def visit_NumberNode(self, node):
        """just return the number"""
        return node.value
    
    def visit_BinaryOpNode(self, node):
        """execute the operation and return its value"""
        left_val = self.visit(node.left)   # Get left side value
        right_val = self.visit(node.right) # Get right side value
        
        # Do the operation
        if node.operator.type == TokenType.PLUS:
            return left_val + right_val
        elif node.operator.type == TokenType.MINUS:
            return left_val - right_val
