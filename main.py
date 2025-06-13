from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_statements = [
        'print(42)',  
        'print(5, 10, 15)',
        'print(abs(-5) + max(1, 2))', 
        'x = min(10, 20, 5)',       
        'print(x)',                 
        'print(x * 2)',               
        'print(min(abs(-10), max(1, 2)))', 
        'y = abs(min(-5, -10))',           
        'print(y)',                      
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
            print(f"Result: {result}")
            if interpreter.variables:
                print(f"Variables: {interpreter.variables}")

        except Exception as E:
            print(f"Error: {E}")


