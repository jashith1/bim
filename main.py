from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_statements = [
        'age = 25',
        'if (age >= 18) { print("You are an adult"), status = "adult" } else { print("You are a minor"), status = "minor" }',
        'print("Status:", status)',
    ]

    
    #same interpreter for all statements because of how memory is handled
    interpreter = Interpreter()
    
    for stmt in test_statements:
        print(f"\nStatement: '{stmt}'")
        
        try:
            lexer = Lexer(stmt)
            parser = Parser(lexer)
            ast = parser.statement()
            print(f"AST: {ast}")
            
            result = interpreter.visit(ast)

            if result is not None:
                print(f"Result: {result}")
            if interpreter.variables:
                print(f"Variables: {interpreter.variables}")

        except Exception as E:
            print(f"Error: {E}")

