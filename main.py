#TO-DO: Arrays, user defined functions, continue and break in loops
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    program =  '''
    for (i in range(10)) {
        if (i == 3) {
            continue
        }
        if (i == 7) {
            break
        }
        print("Number:", i)
    }

    j = 0
    while (j < 10) {
        j = j + 1
        if (j == 5) {
            continue
        }
        if (j == 8) {
            break
        }
        print("While:", j)
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

