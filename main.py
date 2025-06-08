#TO-DO: Add support for negative numbers
from enum import Enum

#Token types recognized by bim
class TokenType(Enum):
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    EOF = "EOF"  # End of file

#Token contains type and actual value
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

# Break input code into tokens
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
    
    def advance(self):
        """Move to the next character"""
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def skip_whitespace(self):
        """Skip spaces and tabs"""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def read_number(self) -> str:
        """Read a number (including decimals)"""
        result = ""
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        """Get the next token from the input"""
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.read_number())
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')
            
            # Throw error if not recognized
            raise Exception(f"Invalid character: {self.current_char}")
        
        # when out of characters return EOF to signify end
        return Token(TokenType.EOF, "")

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



if __name__ == "__main__":
    #bim code is just hard coded for now
    test_expressions = [
        "3",
        "3 + 5",
        "10 - 2",
        "1 + 2 + 3",
        "10 - 3 + 5 - 1",
    ]
    
    for expr in test_expressions:
        print(f"\nParsing: '{expr}'")
        lexer = Lexer(expr)
        parser = Parser(lexer)
        result = parser.expression()
        print(f"Result: {result}")
