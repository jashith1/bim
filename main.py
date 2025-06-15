from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    program =  '''x = 4if (x > 40) 
        {
    print("This is on multiple lines")
    } else {
    print("hi")}'''
    
    

    
    #same interpreter for all statements because of how memory is handled
    interpreter = Interpreter()
    
    print(program)
        
    try:
        lexer = Lexer(program)
        parser = Parser(lexer)
        ast = parser.parse_program()
        print(f"AST: {ast}")
            
        result = interpreter.visit(ast)

        if result is not None:
            print(f"Result: {result}")
        if interpreter.variables:
            print(f"Variables: {interpreter.variables}")

    except Exception as E:
        print(f"Error: {E}")

