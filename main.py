#TO-DO: Add support for negative numbers
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_expressions = [
        "3",
        "3 + 5",
        "10 - 2",
        "1 + 2 + 3",
        "10 - 3 + 5"
    ]
    
    for expr in test_expressions:
        print(f"\nExpression: '{expr}'")
        
        # Parse into AST
        lexer = Lexer(expr)
        parser = Parser(lexer)
        ast = parser.expression()
        print(f"AST: {ast}")
        
        # Execute the AST
        interpreter = Interpreter()
        result = interpreter.visit(ast)
        print(f"Result: {result}")
