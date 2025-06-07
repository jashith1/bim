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


if __name__ == "__main__":
    #bim code is just hard coded for now
    test_expressions = [
        "3 + 5",
        "10 - 2.5",
        "123 + 456 - 789"
    ]
    
    for expr in test_expressions:
        print(f"\nTokenizing: '{expr}'")
        lexer = Lexer(expr)
        
        # Get all tokens until we hit EOF
        tokens = []
        while True:
            token = lexer.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        
        # Print the tokens
        for token in tokens:
            print(f"  {token}")
