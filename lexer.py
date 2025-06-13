from bim_token import TokenType, Token

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
    
    def read_identifier(self):
        """Read a variable name'"""
        result = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def read_string(self):
        """Read a string"""
        result = ""
        self.advance()  # Skip opening quote
        
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                # Handle escape sequences (needs to be added together, wont work as intended if added one character at a time)
                self.advance()
                if self.current_char is None:
                    raise Exception("Unterminated string literal")
                
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == 'r':
                    result += '\r'
                elif self.current_char == '\\':
                    result += '\\'
                elif self.current_char == '"':
                    result += '"'
                else:
                    # For unknown escape sequences, just include the character
                    result += self.current_char
                self.advance()
            else:
                result += self.current_char
                self.advance()
        
        if self.current_char != '"':
            raise Exception("Unterminated string literal")
        
        self.advance()  # Skip closing quote
        return result


    
    def get_next_token(self):
        """Get the next token from the input"""
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.read_number())
            
            if self.current_char == '"':
                return Token(TokenType.STRING, self.read_string())
            
            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/')
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')')
            
            if self.current_char.isalpha() or self.current_char == '_':
                return Token(TokenType.IDENTIFIER, self.read_identifier())
            
            if self.current_char == '=':
                self.advance()
                return Token(TokenType.ASSIGN, '=')
            
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')
            
            # Throw error if not recognized
            raise Exception(f"Invalid character: {self.current_char}")
        
        # when at end return EOF
        return Token(TokenType.EOF, "")
