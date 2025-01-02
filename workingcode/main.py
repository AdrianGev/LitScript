from lexer import lexer
from parser import Parser
from interpreter import Interpreter

def main():
    # Example code using Gooava syntax
    code = '''
    % Declare some variables
    integerNamed <counter> hasTheValueOf <5>#
    textValueNamed <greeting> hasTheValueOf <"Hello, World!">#
    
    % Define a function
    functionNamed <sayHello> withParameters <name> {
        print <"Hello, "> toterminal#
        print <name> toterminal#
    }
    
    % Call the function
    callFunction <sayHello> withArguments <"Alice">#
    
    % If condition example
    ifCondition <counter < 10> isTrue {
        print <"Counter is less than 10!"> toterminal#
    }
    '''

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
    
    print("\nRegular Output:")
    print("-------------")
    for item in result:
        if isinstance(item, list):
            for subitem in item:
                if subitem.startswith("Output:"):
                    print(subitem[8:].strip())  # Remove "Output: " prefix
        elif isinstance(item, str) and item.startswith("Output:"):
            print(item[8:].strip())  # Remove "Output: " prefix

if __name__ == "__main__":
    main()
