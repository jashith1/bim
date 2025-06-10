from bim_token import TokenType
from ast_nodes import BinaryOpNode, NumberNode

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        """Move forward if everything is correct"""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")
    
    def factor(self):
        """Parse a number and move forward"""
        token = self.current_token
        self.eat(TokenType.NUMBER)
        return NumberNode(float(token.value))
    
    def expression(self):
        """Parse the expression and return its AST"""
        node = self.factor()
        
        # build the tree
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            #create the operation AST
            node = BinaryOpNode(left=node, operator=token, right=self.factor())
        
        return node