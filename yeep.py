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

...
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

Digits = '0123456789.'


class Tokens:

    def __init__(self, type, value=None):
        self.type = type
        self.value = value


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
    
        def __init__(self, text):
            self.text = text
            self.pos = -1
            self.current_char = None
            self.advance()
    
    
        def advance(self):
            self.pos += 1
            self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    
        def make_tokens(self):
            tokens = []
    
            while self.current_char != None:
                if self.current_char in ' \t':
                    self.advance()
                elif self.current_char in '0123456789':
                    tokens.append(self.make_number())
                elif self.current_char == '+':
                    tokens.append(Tokens(TT_PLUS))
                    self.advance()
                elif self.current_char == '-':
                    tokens.append(Tokens(TT_MINUS))
                    self.advance()
                elif self.current_char == '*':
                    tokens.append(Tokens(TT_MUL))
                    self.advance()
                elif self.current_char == '/':
                    tokens.append(Tokens(TT_DIV))
                    self.advance()
                elif self.current_char == '(':
                    tokens.append(Tokens(TT_LPAREN))
                    self.advance()
                elif self.current_char == ')':
                    tokens.append(Tokens(TT_RPAREN))
                    self.advance()
                else:
                    char = self.current_char
                    self.advance()
                    return [], Exception(f"Illegal character '{char}'")
    
            return tokens, None
    
    
        def make_number(self):
            num_str = ''
            dot_count = 0
    
            while self.current_char != None and self.current_char in Digits:
                if self.current_char == '.':
                    if dot_count == 1: break
                    dot_count += 1
                    num_str += '.'
                else:
                    num_str += self.current_char
                self.advance()
    
            if dot_count == 0:
                return Tokens(TT_INT, int(num_str))
            else:
                return Tokens(TT_FLOAT, float(num_str))
            
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
            
class Parser:
     
        def __init__(self, tokens):
            self.tokens = tokens
            self.token_index = -1
            self.advance()
        
        def advance(self):
            self.token_index += 1
            self.current_token = self.tokens[self.token_index] if self.token_index < len(self.tokens) else None
        
        def parse(self):
            res = self.expr()
            if not res.error and self.current_token.type != TT_EOF:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected '+', '-', '*' or '/'"
                ))
            return res
        
        def factor(self):
            res = ParseResult()
            token = self.current_token
        
            if token.type in (TT_PLUS, TT_MINUS):
                res.register_advancement()
                self.advance()
                factor = res.register(self.factor())
                if res.error: return res
                return res.success(UnaryOpNode(token, factor))
        
            elif token.type in (TT_INT, TT_FLOAT):
                res.register_advancement()
                self.advance()
                return res.success(NumberNode(token))
        
            elif token.type == TT_LPAREN:
                res.register_advancement()
                self.advance()
                expr = res.register(self.expr())
                if res.error: return res
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
        
        def term(self):
            return self.bin_op(self.factor, (TT_MUL, TT_DIV))
        
        def expr(self):
            return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
        
        def bin_op(self, func, ops):
            res = ParseResult()
            left = res.register(func())
            if res.error: return res
        
            while self.current_token.type in ops:
                op_token = self.current_token
                res.register_advancement()
                self.advance()
                right = res.register(func())
                if res.error: return res
                left = BinOpNode(left, op_token, right)
        
            return res.success(left)
        
        def parse_variable(self, token):
            res = ParseResult()
            self.advance()
            return res.success(VarAccessNode(token))
        

            
       
        

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


 
#################################################################################################
#####   PARSE RESULT
#####   The parse result is a data structure that contains the result of the parse.
#####   The parse result is a data structure that contains the result of the parse.
#################################################################################################
        
class ParseResult:
    
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

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    return tokens, error
    # if error: return None, error
    # parser = Parser(tokens)
    # ast = parser.parse()
    
    # return ast.node, ast.error

