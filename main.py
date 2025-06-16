from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    program =  '''
    score = 77
    if (score == 100) 
    {
        print("perfect score!")
    } else if (score > 90){
        print("A!")
    } 
    else    if   (score > 80)   {
        print("B!")
      } else if(score > 70){
    print("C!")
    }
    else {
    print("fail")
        }'''
    
    

    
    #same interpreter for all statements because of how memory is handled``
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

