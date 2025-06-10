#TO-DO: Add support for negative numbers
from enum import Enum
from lexer import Lexer
from parser import Parser

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
