#Token types recognized by bim
from enum import Enum

class TokenType(Enum):
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    EOF = "EOF"  # End of file
