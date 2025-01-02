import re

# Define token types and their patterns
TOKEN_TYPES = {
    'KEYWORD': r'\b(functionNamed|withParameters|callFunction|return|withArguments)\b',
    'NUMBER': r'\d+(\.\d+)?',
    'STRING': r'"[^"]*"',
    'NAME': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'OPERATOR': r'[=]',
    'BRACKET': r'[<>]',
    'BRACE': r'[{}]',
    'COMMA': r',',
    'WHITESPACE': r'\s+',
    'COMMENT': r'%.*',
}

# Combine all token patterns
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

def lexer(code):
    """Tokenize the input code."""
    tokens = []
    for match in re.finditer(token_regex, code):
        token_type = match.lastgroup
        token_value = match.group()
        if token_type != 'WHITESPACE':  # Skip whitespace
            tokens.append((token_type, token_value))
    return tokens
