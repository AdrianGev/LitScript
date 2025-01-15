import re

class Interpreter:
    def __init__(self):
        self.functions = {}
        self.variables = {}

    def visit(self, node):
        if isinstance(node, list):
            results = []
            for n in node:
                result = self.visit(n)
                if result is not None:
                    results.append(result)
            return results

        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Function(self, node):
        # Store the function definition in the interpreter's function table
        self.functions[node.name] = node
        return f"Function '{node.name}' defined."

    def visit_Call(self, node):
        # Find the function definition
        func = self.functions.get(node.name)
        if not func:
            raise Exception(f"Function '{node.name}' is not defined.")

        # Check arguments and execute the function body
        if len(func.parameters) != len(node.arguments):
            raise Exception(f"Function '{node.name}' expects {len(func.parameters)} arguments, got {len(node.arguments)}.")

        # Bind arguments to parameters
        old_vars = self.variables.copy()
        for param, arg in zip(func.parameters, node.arguments):
            self.variables[param] = arg

        # Execute the function body
        results = []
        for stmt in func.body:
            result = self.visit(stmt)
            if result is not None:
                results.append(result)

        # Restore old variables
        self.variables = old_vars
        return results

    def visit_Return(self, node):
        # Return the evaluated value of the return statement
        return node.value

    def visit_Print(self, node):
        # Handle print statement
        if node.expression is not None:
            # Handle arithmetic expression
            result = self.evaluate_arithmetic(node.expression)
            return f"Output: {result}"
        if node.is_variable:
            if node.value not in self.variables:
                raise Exception(f"Variable '{node.value}' is not defined")
            value = self.variables[node.value]
        else:
            value = node.value
        return f"Output: {value}"

    def visit_VariableDeclaration(self, node):
        # Store variable in the interpreter's variable table
        if node.var_type == 'integerNamed':
            self.variables[node.name] = int(node.value)
        elif node.var_type == 'textValueNamed':
            self.variables[node.name] = node.value
        return f"Variable '{node.name}' defined with value: {node.value}"

    def visit_IfCondition(self, node):
        # Evaluate condition
        condition = self.evaluate_condition(node.condition)
        if condition:
            return self.visit(node.body)
        return None

    def evaluate_condition(self, condition):
        # Simple condition evaluation
        parts = condition.split()
        if len(parts) == 3:
            left, op, right = parts
            left_val = int(self.variables.get(left, left))
            right_val = int(right)
            if op == '<':
                return left_val < right_val
            elif op == '>':
                return left_val > right_val
            elif op == '==':
                return left_val == right_val
        return False

    def evaluate_arithmetic(self, expression):
        """Evaluates arithmetic expressions like '1+2', '5*3', 'x+5', etc."""
        try:
            # Replace variable names with their values
            for var_name, var_value in self.variables.items():
                # Only replace full variable names, not parts of other names
                expression = re.sub(r'\b' + var_name + r'\b', str(var_value), expression)
            
            # Basic security check to ensure only allowed operations
            allowed_chars = set('0123456789+-*/%^() .')
            if not all(c in allowed_chars for c in expression):
                raise Exception("Invalid characters in arithmetic expression")
            
            # Handle power operator (^) by replacing with Python's **
            expression = expression.replace('^', '**')
            
            # Evaluate the expression
            result = eval(expression)  # In a production environment, use a safer evaluation method
            
            # Format the result based on its type
            if isinstance(result, (int, float)):
                if result.is_integer():
                    return int(result)
                return round(result, 6)  # Limit decimal places for floats
            
            raise Exception("Invalid result type")
            
        except Exception as e:
            raise Exception(f"Invalid arithmetic expression: {expression}. Error: {str(e)}")

    def interpret(self, ast):
        return self.visit(ast)

# Example AST node classes (simplified)
class ASTNode: pass

class Function(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class AnonymousFunction(ASTNode):
    def __init__(self, parameters, body, variable_name):
        self.parameters = parameters
        self.body = body
        self.variable_name = variable_name

class HigherOrderFunction(ASTNode):
    def __init__(self, name, func_param, value_param, body):
        self.name = name
        self.func_param = func_param
        self.value_param = value_param
        self.body = body

class Call(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class Return(ASTNode):
    def __init__(self, value):
        self.value = value

class Print(ASTNode):
    def __init__(self, value, is_variable=False, expression=None):
        self.value = value
        self.is_variable = is_variable
        self.expression = expression

class VariableDeclaration(ASTNode):
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value

class IfCondition(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
