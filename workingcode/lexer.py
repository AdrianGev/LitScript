import re

# Define token types and their patterns
TOKEN_TYPES = {
    'KEYWORD': r'\b(print|toterminal|functionNamed|withParameters|callFunction|return|withArguments|integerNamed|textValueNamed|hasTheValueOf|ifCondition|isTrue)\b',
    'NUMBER': r'\d+(\.\d+)?',
    'STRING': r'"[^"]*"',
    'NAME': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'OPERATOR': r'[=]',
    'COMPARISON': r'[<>]=?',  # For actual comparison operators in conditions
    'BRACKET': r'[<>]',  # For syntax delimiters
    'BRACE': r'[{}]',
    'COMMA': r',',
    'TERMINATOR': r'#',
    'COMMENT': r'%[^\n]*',
    'WHITESPACE': r'[\s\n]+',
}

# Combine all token patterns
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

def lexer(code):
    """Tokenize the input code."""
    tokens = []
    bracket_stack = []  # Keep track of bracket context
    
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        token_value = match.group()
        
        # Skip whitespace and comments
        if token_type in ['WHITESPACE', 'COMMENT']:
            continue
            
        # Handle brackets and comparisons
        if token_type in ['COMPARISON', 'BRACKET'] and token_value in ['<', '>']:
            prev_token = tokens[-1] if tokens else None
            
            # Opening bracket cases
            if token_value == '<':
                if prev_token and (prev_token[0] == 'KEYWORD' or 
                                 prev_token[1] in ['hasTheValueOf', 'withParameters', 'withArguments']):
                    token_type = 'BRACKET'
                    bracket_stack.append(True)  # Mark that we're inside a bracket pair
                elif bracket_stack:  # We're inside a bracket pair, must be comparison
                    token_type = 'COMPARISON'
                else:
                    token_type = 'BRACKET'
                    bracket_stack.append(True)
                    
            # Closing bracket cases
            elif token_value == '>':
                if bracket_stack:
                    token_type = 'BRACKET'
                    bracket_stack.pop()
                else:
                    token_type = 'COMPARISON'
                
        tokens.append((token_type, token_value))
    return tokens
