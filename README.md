# Yeep Programming Language

This is a simple programming language interpreter for basic arithmetic operations. The interpreter includes a lexer, parser, and abstract syntax tree (AST) nodes for performing arithmetic operations.

## Getting Started

1. Create a file called `yeep.py`.
2. Copy the provided code into the file.
3. Run the file with Python3 using the command `python3 yeep.py`.
4. Type in an expression (e.g., `2 + 2`) and press enter.
5. The interpreter will print the result of the expression.

## Tokens

- `TT_PLUS`: Represents the plus operator '+'
- `TT_MINUS`: Represents the minus operator '-'
- `TT_DIV`: Represents the division operator '/'
- `TT_MUL`: Represents the multiplication operator '*'
- `TT_LPAREN`: Represents the left parenthesis '('
- `TT_RPAREN`: Represents the right parenthesis ')'
- `TT_INT`: Represents an integer number
- `TT_FLOAT`: Represents a floating-point number
- `TT_EOF`: Represents the end of the file

## Classes

- `Tokens`: Represents a token with a type and optional value
- `Lexer`: Converts source code into tokens
- `NumberNode`: Represents a number in the AST
- `BinOpNode`: Represents a binary operation in the AST
- `UnaryOpNode`: Represents a unary operation in the AST
- `VarAccessNode`: Represents a variable access in the AST
- `Parser`: Converts tokens into an AST
- `Error`: Base class for different types of errors
- `IllegalCharError`: Represents an error for encountering an illegal character
- `InvalidSyntaxError`: Represents an error for encountering invalid syntax
- `ExpectedTokenError`: Represents an error for expecting a specific token
- `Position`: Represents the position of a character in the source code

## Usage Example

```python
# Example usage in the shell
import yeep

while True:
    text = input("yeep >> ")
    result = yeep.run("<stdin>", text)

    if isinstance(result, tuple):
        ast, error = result
        if error:
            print(error.as_string())
        else:
            print(ast)
