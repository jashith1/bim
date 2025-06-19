#TO-DO: user defined functions
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    program =  '''
        numbers = [1, 2, 3, 4, 5]

        print("First number:", numbers[0])

        numbers[1] = 99
        print("Modified array:", numbers)

        numbers.push(6)
        print("After push:", numbers)

        last = numbers.pop()
        print("Popped:", last)
        print("After pop:", numbers)
        print("Array length:", numbers.length())

        for (num in numbers) {
            print("number:", num)
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

