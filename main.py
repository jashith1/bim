from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_statements = [
        'print(true)',                      
        'print(false)',                     
        'is_ready = true',                  
        'print("Ready:", is_ready)',     
        '5 == 5',                       
        '5 != 3',                           
        '3 < 5',                         
        '5 > 3',                        
        '"hello" == "hello"',           
        '"hello" != "world"',       
        '5 == "5"',                       
        'x = 10',
        'y = 5',
        'print(x > y)',                     
        'print(x * 2 == 20)',            
        'print(len("hello") < 10)',       
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

