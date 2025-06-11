from bim_token import TokenType, Token
from ast_nodes import BinaryOpNode, NumberNode, VariableNode, AssignmentNode

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
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumberNode(float(token.value))
        
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return VariableNode(token.value)
        
        raise Exception(f"Unexpected token: {token.type}")

    
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
    
    def statement(self):
        """Parse a statement (ie assignment or expression)"""
        if self.current_token.type == TokenType.IDENTIFIER:
            #temporarily store the data
            saved_lexer_pos = self.lexer.pos
            saved_lexer_char = self.lexer.current_char
            var_name = self.current_token.value
            
            self.eat(TokenType.IDENTIFIER)
            
            if self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                value = self.expression()
                return AssignmentNode(var_name, value)
            else:
                # Not an assignment, restore state and parse as expression
                self.lexer.pos = saved_lexer_pos
                self.lexer.current_char = saved_lexer_char
                self.current_token = Token(TokenType.IDENTIFIER, var_name)
        
        # Parse as expression
        return self.expression()
