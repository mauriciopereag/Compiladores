import ply.lex as lex

reserved = {
    'programa': 'PROGRAMA',
    'inicio':   'INICIO',
    'fin':      'FIN',
    'vars':     'VARS',
    'entero':   'ENTERO',
    'flotante': 'FLOTANTE',
    'nula':     'NULA',
    'si':       'SI',
    'sino':     'SINO',
    'mientras': 'MIENTRAS',
    'haz':      'HAZ',
    'escribe':  'ESCRIBE',
    'retorna': 'RETORNA',
}

tokens = list(reserved.values()) + [
    'ID', 'CTE_ENT', 'CTE_FLOT', 'LETRERO',
    'ASIGNA', 'IGUAL', 'DIF', 'MAYOR', 'MENOR',
    'SUMA', 'RESTA', 'MULT', 'DIV',
    'PARIZQ', 'PARDER', 'LLAVEIZQ', 'LLAVEDER',
    'PUNTOYCOMA', 'COMA', 'DOSPUNTOS',
]

t_IGUAL      = r'=='
t_DIF        = r'!='
t_MAYOR      = r'>'
t_MENOR      = r'<'
t_ASIGNA     = r'='
t_SUMA       = r'\+'
t_RESTA      = r'-'
t_MULT       = r'\*'
t_DIV        = r'/'
t_PARIZQ     = r'\('
t_PARDER     = r'\)'
t_LLAVEIZQ   = r'\{'
t_LLAVEDER   = r'\}'
t_PUNTOYCOMA = r';'
t_COMA       = r','
t_DOSPUNTOS  = r':'
t_ignore     = ' \t'

def t_CTE_FLOT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_LETRERO(t):
    r'"[^"]*"'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"  Token no reconocido: '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

import sys
def get_lexer():
    return lex.lex(module=sys.modules[__name__])