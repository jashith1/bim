from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

if __name__ == "__main__":
    program = '''
        function add(a, b) {
            return a + b
        }
        
        function greet(name) {
            print("Hello", name)
            return "greeting sent"
        }
        
        function factorial(n) {
            if (n <= 1) {
                return 1
            }
            return n * factorial(n - 1)
        }
        
        result = add(5, 3)
        print("5 + 3 =", result)
        
        msg = greet("bruh")
        print("Function returned:", msg)
        
        fact = factorial(5)
        print("5! =", fact)
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

