"""
This file contains the implementation of a simple programming language interpreter.
The interpreter includes a lexer, parser, and AST nodes for performing arithmetic operations.

To use this interpreter:
1. Create a file called yeep.py
2. Copy the code below into the file
3. Run the file with python3 yeep.py
4. Type in an expression like 2 + 2 and press enter
5. The interpreter will print the result of the expression

Tokens:
- TT_PLUS: Represents the plus operator '+'
- TT_MINUS: Represents the minus operator '-'
- TT_DIV: Represents the division operator '/'
- TT_MUL: Represents the multiplication operator '*'
- TT_LPAREN: Represents the left parenthesis '('
- TT_RPAREN: Represents the right parenthesis ')'
- TT_INT: Represents an integer number
- TT_FLOAT: Represents a floating-point number
- TT_EOF: Represents the end of the file

Classes:
- Tokens: Represents a token with a type and optional value
- Lexer: Converts source code into tokens
- NumberNode: Represents a number in the abstract syntax tree (AST)
- BinOpNode: Represents a binary operation in the AST
- UnaryOpNode: Represents a unary operation in the AST
- VarAccessNode: Represents a variable access in the AST
- Parser: Converts tokens into an AST
- Error: Base class for different types of errors
- IllegalCharError: Represents an error for encountering an illegal character
- InvalidSyntaxError: Represents an error for encountering invalid syntax
- ExpectedTokenError: Represents an error for expecting a specific token
- Position: Represents the position of a character in the source code
"""
"""
This file contains the implementation of a simple programming language interpreter.
The interpreter includes a lexer, parser, and AST nodes for performing arithmetic operations.
"""

################################################################################################
#####                     THIS IS WHERE WE WRITE THE PROGRAM INSTRUCTIONS                  #####
################################################################################################


#################################################################################################
#####   TOKENS
#####   Tokens are the smallest unit of a program that have meaning.
#####   Tokens are the words and symbols that make up a program.
#################################################################################################


TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_DIV = 'DIV'
TT_MUL = 'MUL'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_EOF = 'EOF'
TT_POWER = 'EXPONENTIAL'


#########################################
###     CONSTANTS
#########################################

DEBUG = False
DIGITS = '0123456789.'




class Tokens:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value
        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

    


#################################################################################################
#####   LEXER
#####   The lexer takes the source code and converts it into tokens.
#####   The lexer is also called a tokenizer or scanner.
#################################################################################################
    
class Lexer:
    """
    Lexer class for tokenizing input text.
    """

    def __init__(self, fn, text):
        """
        Initialize the Lexer object.

        Parameters:
        - fn (str): The filename or filepath associated with the input text.
        - text (str): The input text to be tokenized.
        """
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        """
        Advance the current character pointer to the next character in the input text.
        """
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        """
        Tokenize the input text and return a list of tokens.

        Returns:
        - tokens (list): A list of tokens.
        - error (Exception or None): An error message if encountered during tokenization, or None if no error occurred.
        """
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in '0123456789':
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Tokens(TT_PLUS, pos_start= self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Tokens(TT_MINUS, pos_start= self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Tokens(TT_MUL, pos_start= self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Tokens(TT_DIV, pos_start= self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Tokens(TT_LPAREN, pos_start= self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Tokens(TT_RPAREN, pos_start= self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], Exception(pos_start, self.pos, f"Illegal character '{char}'")

        tokens.append(Tokens(TT_EOF, pos_start = self.pos))

        return tokens, None

    def make_number(self):
        """
        Tokenize a number and return the corresponding token.

        Returns:
        - token (Tokens): The token representing the number.
        """
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS:
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Tokens(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Tokens(TT_FLOAT, float(num_str), pos_start, self.pos)

            

            
#################################################################################################
#####   NODES
#####   Nodes are the building blocks of the AST.
#####   Nodes are the data structures that represent the code.
#####   Nodes are the data structures that represent the code.
#################################################################################################
            
class NumberNode:
        
        def __init__(self, token):
            self.token = token
        
        def __repr__(self) -> str:
            return f'{self.token}'
        
class BinOpNode:
            
            def __init__(self, left_node, op_token, right_node):
                self.left_node = left_node
                self.op_token = op_token
                self.right_node = right_node
            
            def __repr__(self) -> str:
                return f'({self.left_node}, {self.op_token}, {self.right_node})'
            
class UnaryOpNode:
                
                def __init__(self, op_token, node):
                    self.op_token = op_token
                    self.node = node
                
                def __repr__(self) -> str:
                    return f'({self.op_token}, {self.node})'
                
class VarAccessNode:
                        
                        def __init__(self, token):
                            self.token = token
                        
                        def __repr__(self) -> str:
                            return f'{self.token}'
            
#################################################################################################
#####   PARSER
#####   The parser takes the tokens and converts them into an AST.
#####   The parser is also called a syntactic analyzer.
#################################################################################################
            
# Updated Parser class with operator precedence

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        """
        Advances the token index and sets the current_token attribute to the next token in the list of tokens.
        """
        self.token_index += 1
        self.current_token = self.tokens[self.token_index] if self.token_index < len(self.tokens) else None

    def parse(self):
        """
        Parses the tokens and returns the resulting parse tree.
        """
        return self.expr()

    def factor(self):
        """
        Parses a factor expression and returns the corresponding parse tree node.
        """
        res = ParseResult()
        token = self.current_token

        if token.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        elif token.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        elif token.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected int or float"
        ))

    def power(self):
        """
        Parses a power expression and returns the corresponding parse tree node.
        """
        return self.bin_op(self.factor, (TT_POWER, ), self.factor)

    def term(self):
        """
        Parses a term expression and returns the corresponding parse tree node.
        """
        return self.bin_op(self.power, (TT_MUL, TT_DIV), self.factor)

    def expr(self):
        """
        Parses an expression and returns the corresponding parse tree node.
        """
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS), self.term)

    def bin_op(self, func_a, ops, func_b):
        """
        Parses a binary operation expression and returns the corresponding parse tree node.
        """
        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_token.type in ops:
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_token, right)

        return res.success(left)
    

        
        
        

            
       
        

#################################################################################################
#####   ERROR
#####   The error class is used to handle errors.
#####   The error class is used to handle errors.
#################################################################################################
               

class Error:
        
        def __init__(self, pos_start, pos_end, error_name, details):
            self.pos_start = pos_start
            self.pos_end = pos_end
            self.error_name = error_name
            self.details = details
        
        def as_string(self):
            result = f'{self.error_name}: {self.details}\n'
            result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
            return result
        
        def __repr__(self) -> str:
            return f'{self.as_string()}'
        
class IllegalCharError(Error):

        def __init__(self, pos_start, pos_end, details):
            super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):

        def __init__(self, pos_start, pos_end, details):
            super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class ExpectedTokenError(Error):
     
        def __init__(self, pos_start, pos_end, details):
            super().__init__(pos_start, pos_end, 'Expected Token', details)


class Position:
    """
    Represents a position in a file.
    
    Attributes:
        idx (int): The index of the position.
        ln (int): The line number of the position.
        col (int): The column number of the position.
        fn (str): The file name.
        ftxt (str): The file text.
    """
     
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    
    def advance(self, current_char = None):
        """
        Advances the position by one character.
        
        Args:
            current_char (str, optional): The current character. Defaults to None.
        
        Returns:
            Position: The updated position.
        """
        self.idx += 1
        self.col += 1
        
        if current_char is not None and current_char == '\n':
            self.ln += 1
            self.col = 0
        
        return self
    
    def copy(self):
        """
        Creates a copy of the position.
        
        Returns:
            Position: The copied position.
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the position.
        
        Returns:
            str: The string representation of the position.
        """
        return f'{self.idx}:{self.ln}:{self.col}:{self.fn}:{self.ftxt}'
        




 
#################################################################################################
#####   PARSE RESULT
#####   The parse result is a data structure that contains the result of the parse.
#####   The parse result is a data structure that contains the result of the parse.
#################################################################################################
        
class ParseResult:
    """
    Represents the result of a parsing operation.
    
    Attributes:
        error: An error message if the parsing operation encountered an error, otherwise None.
        node: The parsed node if the parsing operation was successful, otherwise None.
        advance_count: The number of tokens advanced during the parsing operation.
    """
    
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
    
    def register_advancement(self):
        self.advance_count += 1
    
    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node
    
    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
    

    
#################################################################################################
#####   RUN
#####   The run function is the main function of the interpreter.
#####   The run function is the main function of the interpreter.
#################################################################################################

def run(fn, text):
    """
    Executes the given code by performing lexical analysis, tokenization, and parsing.

    Args:
        fn (str): The filename or path of the source code file.
        text (str): The source code to be executed.

    Returns:
        tuple: A tuple containing the abstract syntax tree (AST) node and any error encountered during parsing.
               If no error occurred, the error value will be None.
    """
    lexer = Lexer(fn, text)
    error = lexer.make_tokens()
    if error:
        return None, error
    parser = Parser(lexer.tokens)
    ast = parser.parse()
    return ast.node, ast.error


