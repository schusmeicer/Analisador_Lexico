import sys
from typing import NamedTuple
from typing import Union

ERRO = 0
IDENTIF = 1
RESERVADA = 2
NUM_INT = 3
NUM_REAL = 4
OPREL = 5 
OPARIT = 6
EOS = 7

token_msg = [ "ERRO", "IDENTIF", "RESERVADA", "NUMINT", "NUMREAL", "OPREL", "OPARIT", "EOS" ]

class Token(NamedTuple):
    tipo: int
    lexema: str
    valor: Union[int, float]
    linha: int

class AnalisadorLexico:
    def __init__(self, buffer):
        self.buffer = buffer + '\0'
        self.nlinha = 1
        self.i = 0

    def retract_char(self):
        self.i -= 1

    def proximo_char(self):
        c = self.buffer[self.i]
        self.i += 1
        return c
    
    def proximo_token(self):
        token = ERRO
        c = self.proximo_char()
        while (c in  [' ', '\n','\0']):
            if (c == '\n'):
                self.nlinha += 1
            if (c == '\0'):
                return Token(EOS, '', 0, self.nlinha)
            c = self.proximo_char()
        if (c.isalpha()):
            token = self.reconhece_ID()
        elif (c.isdigit()):
            token = self.reconhece_NUM()
        elif (self.is_Arit()):
            token = self.reconhece_Arit()
        else:
            token = self.reconhece_Rel()
        return token

    def is_Arit(self):
        lexema = self.buffer[self.i - 1]
        return lexema in ['+', '-', '*', '/', '%']
    
    def reconhece_Arit(self):
        lexema = self.buffer[self.i - 1]
        estado = 1
        while True:
            if estado == 1:
                c = self.proximo_char()
                if lexema in ['+', '-']:
                    if c == '=':
                        lexema += c
                    return Token(OPARIT, lexema, 0, self.nlinha)
                estado = 2
            elif estado == 2:
                if lexema == '*':
                    if c == '*' or c == '=':
                        lexema += c
                    return Token(OPARIT, lexema, 0, self.nlinha)
                elif lexema == '/':
                    if c == '/' or c == '=':
                        lexema += c
                    return Token(OPARIT, lexema, 0, self.nlinha)
                elif lexema == '%':
                    if c == '=':
                        lexema += c
                    return Token(OPARIT, lexema, 0, self.nlinha)
                return Token(ERRO, '', 0, self.nlinha)

    def reconhece_Rel(self):
        lexema = self.buffer[self.i - 1]
        estado = 1
        while True:
            if estado == 1:
                c = self.proximo_char()
                if lexema in ['>','<']:
                    if c == "=":
                        lexema += c
                    return Token(OPREL, lexema, 0, self.nlinha)
                elif lexema in ['!','=']:
                    estado = 2
                else:
                    return Token(ERRO, '', 0, self.nlinha)
            elif estado == 2:
                if c == "=":
                    lexema += c
                    return Token(OPREL, lexema, 0, self.nlinha)
                else:
                    return Token(ERRO, '', 0, self.nlinha)    
    def reconhece_ID(self):
        lexema = self.buffer[self.i - 1]
        palavras_reservadas = ['and','as','assert','break',
        'class','continue','def','del','elif','else','except'
        'False' 'finally','for','from','global','if','import',
        'in','is','lambda','None','nonlocal','not','or','pass',
        'raise','return','True','try','while','with','yield']
        c = self.proximo_char()
        while (c.isalpha() or c.isdigit()):
            lexema = lexema + c
            c = self.proximo_char()
        self.retract_char()
        if lexema in palavras_reservadas:
            return Token(RESERVADA, lexema, 0, self.nlinha)
        return Token(IDENTIF, lexema, 0, self.nlinha)

    def reconhece_NUM(self):
        lexema = self.buffer[self.i - 1]
        print("lexema = ", lexema)
        estado = 1  
        while True:
            if estado == 1:
                c = self.proximo_char()
                if (c == '.'):                 
                    lexema = lexema + c
                    estado = 3               
                elif (c.isdigit()): 
                    lexema = lexema + c
                    estado = 1
                elif (not c.isalpha()):
                    return Token(NUM_INT, lexema, int(lexema), self.nlinha)
                else:
                    return Token(ERRO, '', 0, self.nlinha)
            elif estado == 3:
                c = self.proximo_char()
                if c.isdigit(): 
                    lexema = lexema + c
                    estado = 4
                else:
                    return Token(ERRO, '', 0, self.nlinha)        
            elif estado == 4:
                c = self.proximo_char()  
                if c.isdigit(): 
                    lexema = lexema + c
                    estado = 4                   
                elif not c.isalpha():
                    return Token(NUM_REAL, lexema, float(lexema), self.nlinha)
                else:
                    return Token(ERRO, '', 0, self.nlinha)

def leia_arquivo():
    if len(sys.argv) > 1:
        arquivo = open(sys.argv[1], 'r')
    else:
        arquivo = open('entrada.txt', 'r')
    buffer = arquivo.read()    
    arquivo.close()
    return buffer

def main():
    buffer = buff
    lex = AnalisadorLexico(buffer)
    token = lex.proximo_token()
    print(token)
    while (token.tipo != EOS and token.tipo != ERRO):
        print("Linha: {}  -  token: {} \tlexema: {} \t\tvalor: \
    {}".format(token.linha, token_msg[token.tipo], token.lexema, token.valor))
        token = lex.proximo_token()
    print("Linha: {}  -  token: {} \tlexema: {} \t\tvalor: \
    {}".format(token.linha, token_msg[token.tipo], token.lexema, token.valor))
buff = """
()
"""
main()