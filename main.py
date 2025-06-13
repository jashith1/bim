from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_statements = [
        '"hello world"',   
        'print("Hello, World!")',     
        'print("hello\nworld")',  
        
        'name = "Ryo"',                  
        'print("Hello,", name)',
        'greeting = "Hi " + name',
        'print(greeting)',
        '"ha" * 3',                      
        '3 * "ho"',                       

        'len("hello")',                   
        'upper("hello")',                  
        'lower("WORLD")',                

        'print("x = " + x + ", x * 2 = " + (x * 2))',
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

