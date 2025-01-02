from lexer import lexer
from parser import Parser
from interpreter import Interpreter

def main():
    code = 'print <"Hello, World!"> toterminal#'
    

    # Tokenize the code
    tokens = lexer(code)
    print("Tokens:", tokens)  # Debugging: print tokens

    # Parse the tokens into an AST
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)  # Debugging: print the AST

    # Interpret the AST
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    print("Result:", result)

if __name__ == "__main__":
    main()
