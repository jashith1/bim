import sys
import os
from bim.lexer import Lexer
from bim.parser import Parser
from bim.interpreter import Interpreter

def read_file(filename):
    """Read the contents of a BIM file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

def run_bim_code(code, filename="<stdin>"):
    """Execute BIM code"""
    interpreter = Interpreter()
    
    try:
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse_program()
        
        result = interpreter.visit(ast)
            
    except Exception as e:
        print(f"Error in {filename}: {e}")
        sys.exit(1)

def run_help():
    print("bim <filename.bim>    # Run a BIM file")

def main():
    if len(sys.argv) < 2:
        run_help()
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "--help" or arg == "-h":
        run_help()
        return
    
    else:
        filename = arg
        
        if not filename.endswith('.bim'):
            print("Warning: BIM files should have a .bim extension")
        
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        
        code = read_file(filename)
        run_bim_code(code, filename)

if __name__ == "__main__":
    main()