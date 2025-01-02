# Abstract Syntax Tree (AST) Node Definitions

class ASTNode:
    """Base class for all AST nodes."""
    pass

class Function(ASTNode):
    """Represents a named function."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"Function(name={self.name}, parameters={self.parameters}, body={self.body})"

class AnonymousFunction(ASTNode):
    """Represents an anonymous function assigned to a variable."""
    def __init__(self, parameters, body, variable_name):
        self.parameters = parameters
        self.body = body
        self.variable_name = variable_name

    def __repr__(self):
        return f"AnonymousFunction(parameters={self.parameters}, body={self.body}, variable_name={self.variable_name})"

class HigherOrderFunction(ASTNode):
    """Represents a function that takes another function as a parameter."""
    def __init__(self, name, func_param, value_param, body):
        self.name = name
        self.func_param = func_param
        self.value_param = value_param
        self.body = body

    def __repr__(self):
        return (f"HigherOrderFunction(name={self.name}, func_param={self.func_param}, "
                f"value_param={self.value_param}, body={self.body})")

class Call(ASTNode):
    """Represents a function call."""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"Call(name={self.name}, arguments={self.arguments})"

class Return(ASTNode):
    """Represents a return statement."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return(value={self.value})"

class Parameter(ASTNode):
    """Represents a parameter in a function definition."""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Parameter(name={self.name}, value={self.value})"

class NestedFunction(ASTNode):
    """Represents a nested function within another function."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"NestedFunction(name={self.name}, parameters={self.parameters}, body={self.body})"
