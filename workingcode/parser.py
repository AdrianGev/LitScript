from ast import Function, Call, Return

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected_type=None):
        token = self.current_token()
        if token and (expected_type is None or token[0] == expected_type):
            self.pos += 1
            return token
        raise ValueError(f"Expected {expected_type}, got {token}")

    def parse(self):
        nodes = []
        while self.current_token():
            token = self.current_token()
            if token[0] == 'KEYWORD':
                if token[1] == 'functionNamed':
                    nodes.append(self.parse_function())
                elif token[1] == 'callFunction':
                    nodes.append(self.parse_call())
                elif token[1] == 'return':
                    nodes.append(self.parse_return())
                else:
                    raise ValueError(f"Unexpected keyword: {token[1]}")
            else:
                raise ValueError(f"Unexpected token: {token}")
        return nodes

    def parse_function(self):
        self.eat('KEYWORD')  # functionNamed
        name = self.eat('NAME')[1]
        self.eat('KEYWORD')  # withParameters
        parameters = self.parse_parameters()
        self.eat('BRACE')  # {
        body = []
        while self.current_token() and self.current_token()[0] != 'BRACE':
            body.append(self.parse())
        self.eat('BRACE')  # }
        return Function(name=name, parameters=parameters, body=body)

    def parse_parameters(self):
        params = {}
        while self.current_token() and self.current_token()[0] not in {'BRACE', 'KEYWORD'}:
            key = self.eat("NAME")[1]
            self.eat("OPERATOR")  # =
            params[key] = self.eat("STRING")[1]
        return params

    def parse_call(self):
        self.eat("KEYWORD")  # callFunction
        name = self.eat("NAME")[1]
        self.eat("KEYWORD")  # withArguments
        arguments = self.parse_arguments()
        return Call(name=name, arguments=arguments)

    def parse_arguments(self):
        args = []
        while self.current_token() and self.current_token()[0] in {"STRING", "COMMA"}:
            if self.current_token()[0] == 'COMMA':
                self.eat('COMMA')  # Skip commas
            else:
                args.append(self.eat("STRING")[1])
        return args

    def parse_return(self):
        self.eat("KEYWORD")  # return
        value = self.eat("STRING")[1]
        return Return(value=value)
