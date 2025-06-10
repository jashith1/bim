from token_type import TokenType

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
        return float(token.value)
    
    def expression(self):
        """Parse the expression (like: number + number, etc)"""
        result = self.factor()
        
        # Keep processing + and - operations
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            print(token, result)
            if token.type == TokenType.PLUS:
                #move forward to number
                self.eat(TokenType.PLUS)
                #get number and move forward to next symbol
                result = result + self.factor()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result = result - self.factor()
        
        return result
