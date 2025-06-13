from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    test_statements = [
        "-5",                  
        "+5",                   
        "--5",        
        "++5",           
        "-5 + 3",  
        "5 + -3",  
        "-(5 + 3)",    
        "-5 * -3",     
        "-(2 + 3) * 4",         
        "-2 * (3 + 4)",         
        "(-2 + 3) * (-4 + 5)",
        "x = -10",             
        "y = -x",     
        "z = -(x + y)"  
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

