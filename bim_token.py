from enum import Enum

#Token contains type and actual value
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

#Token types recognized by bim
class TokenType(Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"   
    DIVIDE = "DIVIDE"      
    LPAREN = "LPAREN" #(
    RPAREN = "RPAREN" #)
    COMMA = "COMMA"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    ELIF = "ELIF" #note: lexer expects `else if` and not `elif`
    LBRACE = "LBRACE" #{
    RBRACE = "RBRACE" #}
    SEMICOLON = "SEMICOLON"
    NEWLINE = "NEWLINE"
    EOF = "EOF"  # End of file
    IDENTIFIER = "IDENTIFIER" #variable names
    ASSIGN = "ASSIGN" #assignment operator (ie the "=" sign)
    #loops
    WHILE = "WHILE"
    FOR = "FOR"
    IN = "IN" # ex: "for x in range(10)"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    DOT = "DOT" #for dot methods (like array.push)
