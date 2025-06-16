#TO-DO: Arrays, user defined functions, continue and break in loops
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    program =  '''
        i = 0
        while (i < 5) {
            print("While loop:", i)
            i = i + 1
        }

        for (x in range(3)) {
            print("For loop:", x)
        }

        for (char in "hello") {
            print("Character:", char)
        }
    '''
    
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

