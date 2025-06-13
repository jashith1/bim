#TO-DO: Add support for negative numbers
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_statements = [
        "(2+ 3) * 4",
        "10 / (2 + 3)",
        "2 * (3 + 4) * 5",
        "x = (2 + 3) * 4",
        "y = (x / 2)",
        "z =( x + y) * 2"
    ]

    #same interpreter for all statements because of how memory is handled
    interpreter = Interpreter()
    
    for stmt in test_statements:
        print(f"\nStatement: '{stmt}'")
        
        lexer = Lexer(stmt)
        parser = Parser(lexer)
        ast = parser.statement()
        print(f"AST: {ast}")
        
        result = interpreter.visit(ast)
        print(f"Result: {result}")
        if interpreter.variables:
            print(f"Variables: {interpreter.variables}")

