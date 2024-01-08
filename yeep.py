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


class Tokens:

    def __init__(self, type, value):
        self.type = type
        self.value = value


    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'





