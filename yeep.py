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
TT_INT = 'TT_INT'
TT_FLOAT = 'FLOAT'
TT_EOF = 'EOF'

Digits = '0123456789'


class Tokens:

    def __init__(self, type, value):
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
            
#################################################################################################
#####   PARSER
#####   The parser takes the tokens and converts them into an AST.
#####   The parser is also called a syntactic analyzer.
#################################################################################################
            
class Parser:
     

