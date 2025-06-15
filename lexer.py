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

    def peek(self):
        """Look at the next character without advancing"""
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
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
        """Read a string (or check if provided input is a boolean)"""
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
            if self.current_char in ' \t\r':
                self.skip_whitespace()
                continue
            
            if self.current_char == '\n':
                self.advance()
                return Token(TokenType.NEWLINE, '\n')
            
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
                identifier = self.read_identifier()
                if identifier == 'true':
                    return Token(TokenType.TRUE, True)
                elif identifier == 'false':
                    return Token(TokenType.FALSE, False)
                elif identifier == 'if':
                    return Token(TokenType.IF, 'if')
                elif identifier == 'else':
                    return Token(TokenType.ELSE, 'else')

                return Token(TokenType.IDENTIFIER, identifier)
            
            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQUAL, '==')
                else:
                    self.advance()
                    return Token(TokenType.ASSIGN, '=')
            
            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.NOT_EQUAL, '!=')
                else:
                    raise Exception(f"Invalid character: {self.current_char}")
            
            if self.current_char == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.LESS_EQUAL, '<=')
                else:
                    self.advance()
                    return Token(TokenType.LESS_THAN, '<')
            
            if self.current_char == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.GREATER_EQUAL, '>=')
                else:
                    self.advance()
                    return Token(TokenType.GREATER_THAN, '>')

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',')
            
            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{')
            
            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}')
            
            elif self.current_char == ';':
                return Token(TokenType.EOF, "")
        
        # when at end return EOF
        return Token(TokenType.EOF, "")
