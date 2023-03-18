# --- CPA04_PY030 ---
import sys
from typing import NamedTuple
from typing import Union

ERRO = 0
IDENTIFICADOR = 1
NUM_INT = 2
NUM_REAL = 3
ARIT = 4
EOS = 5

token_msg = ['ERRO', 'IDENTIF', 'NUM_INT', 'NUM_REAL', 'EOS']


class Token(NamedTuple):
    tipo: int
    lexema: str
    valor: Union[int, float]
    linha: int


class Analisador_Lexico:
    def __init__(self, buffer):
        self.nlinha = 1
        self.buffer = buffer + '\0'
        self.i = 0

    def proximo_token(self):
        token = ERRO
        c = self.proximo_char()
        while (c in [' ', '\n', '\0']):
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

        return token

    def reconhece_ID(self):
        lexema = self.buffer[self.i - 1]
        c = self.proximo_char()
        while (c.isalpha() or c.isdigit()):
            lexema = lexema + c
            c = self.proximo_char()
        self.retract_char()
        return Token(IDENTIFICADOR, lexema, 0, self.nlinha)

    def is_Arit(self):
        lexema = self.buffer[self.i - 1]
        if lexema in ['+', '-', '*', '/', '%']:
            return True
        else:
            return False

    def reconhece_Arit(self):
        lexema = self.buffer[self.i - 1]
        c = self.proximo_char()
        if lexema in ['+', '-' '/']:
            if c == '=':
                lexema = + c
                return Token(ARIT, lexema, 4, self.nlinha)
            return Token(ARIT, lexema, 4, self.nlinha)
        elif lexema == '*':
            if c == '*' or c == '=':
                lexema = + c
                return Token(ARIT, lexema, 4, self.nlinha)
            else:
                return Token(ARIT, lexema, 4, self.nlinha)
        elif lexema == '%':
            return Token(ARIT, lexema, 4, self.nlinha)

    def reconhece_NUM(self):
        lexema = self.buffer[self.i - 1]
        print("lexema = ", lexema)
        # c = self.proximo_char()
        # print("c = ", c)
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

    def proximo_char(self):
        c = self.buffer[self.i]
        self.i += 1
        return c

    def retract_char(self):
        self.i -= 1


def leia_arquivo():
    if len(sys.argv) > 1:
        arquivo = open(sys.argv[1], 'r')
    else:
        arquivo = open('FILES/entrada.txt', 'r')
    buffer = arquivo.read()
    arquivo.close()
    return buffer


def main():
    buffer = leia_arquivo()
    lex = Analisador_Lexico(buffer)
    token = lex.proximo_token()
    print(token)
    while (token.tipo != EOS and token.tipo != ERRO):
        print("Linha: {}  -  token: {} \tlexema: {} \t\tvalor: \
{}".format(token.linha, token_msg[token.tipo], token.lexema, token.valor))
        token = lex.proximo_token()
    print("Linha: {}  -  token: {} \tlexema: {} \t\tvalor: \
{}".format(token.linha, token_msg[token.tipo], token.lexema, token.valor))


main()

a = '+'
type(a)
