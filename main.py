#TO-DO: Add support for negative numbers
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_statements = [
        "bruh=5",
        "breh= 3 + 9", 
        "broh=bruh+breh",
        "result = bruh + breh + broh"
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
        print(f"Variables: {interpreter.variables}")

