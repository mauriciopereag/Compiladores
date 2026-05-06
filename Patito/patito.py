import ply.lex as lex
import ply.yacc as yacc

# ─────────────────────────────────── RESERVADAS ─────────────────────────────────

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
}

tokens = list(reserved.values()) + [
    'ID', 'CTE_ENT', 'CTE_FLOT', 'LETRERO',
    'ASIGNA', 'IGUAL', 'DIF', 'MAYOR', 'MENOR',
    'SUMA', 'RESTA', 'MULT', 'DIV',
    'PARIZQ', 'PARDER', 'LLAVEIZQ', 'LLAVEDER',
    'PUNTOYCOMA', 'COMA', 'DOSPUNTOS',
]

# ─────────────────────────────────── LEXER ────────────────────────────────────

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

lexer = lex.lex()

# ─────────────────────────────────── PARSER ───────────────────────────────────

def p_programa(p):
    'programa : PROGRAMA ID PUNTOYCOMA vars_opc funcs_opc INICIO cuerpo FIN'

def p_vars_opc_con(p):
    'vars_opc : vars'

def p_vars_opc_vacio(p):
    'vars_opc : empty'

def p_funcs_opc_con(p):
    'funcs_opc : funcs funcs_opc'

def p_funcs_opc_vacio(p):
    'funcs_opc : empty'

def p_vars(p):
    'vars : VARS lista_ids DOSPUNTOS tipo PUNTOYCOMA'

def p_lista_ids_uno(p):
    'lista_ids : ID'

def p_lista_ids_mas(p):
    'lista_ids : ID COMA lista_ids'

def p_tipo_entero(p):
    'tipo : ENTERO'

def p_tipo_flotante(p):
    'tipo : FLOTANTE'

def p_cuerpo(p):
    'cuerpo : LLAVEIZQ estatutos LLAVEDER'

def p_estatutos_vacio(p):
    'estatutos : empty'

def p_estatutos_con(p):
    'estatutos : estatuto estatutos'

def p_estatuto_asigna(p):
    'estatuto : asigna'

def p_estatuto_condicion(p):
    'estatuto : condicion'

def p_estatuto_ciclo(p):
    'estatuto : ciclo'

def p_estatuto_imprime(p):
    'estatuto : imprime'

def p_estatuto_llamada(p):
    'estatuto : llamada PUNTOYCOMA'

def p_asigna(p):
    'asigna : ID ASIGNA expresion PUNTOYCOMA'

def p_condicion(p):
    'condicion : SI PARIZQ expresion PARDER cuerpo sino_opc'

def p_sino_con(p):
    'sino_opc : SINO cuerpo'

def p_sino_vacio(p):
    'sino_opc : PUNTOYCOMA'

def p_ciclo(p):
    'ciclo : MIENTRAS PARIZQ expresion PARDER HAZ cuerpo PUNTOYCOMA'

def p_imprime(p):
    'imprime : ESCRIBE PARIZQ imprime_items PARDER PUNTOYCOMA'

def p_imprime_items_uno(p):
    'imprime_items : imprime_item'

def p_imprime_items_mas(p):
    'imprime_items : imprime_item COMA imprime_items'

def p_imprime_item_exp(p):
    'imprime_item : expresion'

def p_imprime_item_letrero(p):
    'imprime_item : LETRERO'

def p_expresion_simple(p):
    'expresion : exp'

def p_expresion_mayor(p):
    'expresion : exp MAYOR exp'

def p_expresion_menor(p):
    'expresion : exp MENOR exp'

def p_expresion_igual(p):
    'expresion : exp IGUAL exp'

def p_expresion_dif(p):
    'expresion : exp DIF exp'

def p_exp_termino(p):
    'exp : termino'

def p_exp_suma(p):
    'exp : termino SUMA exp'

def p_exp_resta(p):
    'exp : termino RESTA exp'

def p_termino_factor(p):
    'termino : factor'

def p_termino_mult(p):
    'termino : factor MULT termino'

def p_termino_div(p):
    'termino : factor DIV termino'

def p_factor_paren(p):
    'factor : PARIZQ expresion PARDER'

def p_factor_pos(p):
    'factor : SUMA factor'

def p_factor_neg(p):
    'factor : RESTA factor'

def p_factor_cte_ent(p):
    'factor : CTE_ENT'

def p_factor_cte_flot(p):
    'factor : CTE_FLOT'

def p_factor_id(p):
    'factor : ID'

def p_factor_llamada(p):
    'factor : llamada'

def p_funcs(p):
    'funcs : tipo_ret ID PARIZQ params PARDER LLAVEIZQ vars_opc cuerpo LLAVEDER PUNTOYCOMA'

def p_tipo_ret_nula(p):
    'tipo_ret : NULA'

def p_tipo_ret_tipo(p):
    'tipo_ret : tipo'

def p_params_vacio(p):
    'params : empty'

def p_params_uno(p):
    'params : ID DOSPUNTOS tipo'

def p_params_mas(p):
    'params : ID DOSPUNTOS tipo COMA params'

def p_llamada(p):
    'llamada : ID PARIZQ args PARDER'

def p_args_vacio(p):
    'args : empty'

def p_args_uno(p):
    'args : expresion'

def p_args_mas(p):
    'args : expresion COMA args'

def p_empty(p):
    'empty :'

def p_error(p):
    if p:
        print(f"  Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("  Error de sintaxis: fin de archivo inesperado")

parser = yacc.yacc()

# ─────────────────────────────────── TESTS ──────────────────────────────────────────

test1 = """
programa minimo;
inicio
{ }
fin
"""

test2 = """
programa vars_test;
vars x, y : entero;
inicio
{
    x = 5;
    y = x + 3;
}
fin
"""

test3 = """
programa cond_test;
vars n : entero;
inicio
{
    n = 10;
    si (n > 5) {
        escribe("mayor");
    };
    si (n < 0) {
        escribe("negativo");
    } sino {
        escribe("no negativo");
    }
}
fin
"""

test4 = """
programa ciclo_test;
vars i : entero;
inicio
{
    i = 0;
    mientras (i < 10) haz {
        i = i + 1;
    };
}
fin
"""

test5 = """
programa funcs_test;
nula saluda (nombre : entero) {
    {
        escribe("hola", nombre);
    }
};
inicio
{
    saluda(42);
}
fin
"""

test6 = """
programa flot_test;
vars a, b : flotante;
inicio
{
    a = 3.14;
    b = a * 2.0 + 1.5;
    escribe(b);
}
fin
"""

test_e1 = "programa 123prog;"
test_e2 = "programa p; vars x entero;"
test_e3 = """
programa p;
vars n : entero;
inicio
{ si n > 5 { escribe("mal"); }; }
fin
"""
test_e4 = """
programa p;
vars i : entero;
inicio
{ mientras (i < 10) { i = i + 1; }; }
fin
"""
test_e5 = """
programa p;
vars x : entero;
inicio
{ x = ; }
fin
"""
test_e6 = """
programa p;
inicio
{ }
"""

# ─────────────────────────────────── MAIN ───────────────────────────────────

if __name__ == "__main__":
    print("\n" + "-"*50)
    print("           PATITO COMPILER - TESTS")
    print("-"*50)

    print("\n──── CASOS VÁLIDOS ────")
    for nombre, codigo in [
        ("Test 1 - Programa mínimo",                    test1),
        ("Test 2 - Variables y asignación",             test2),
        ("Test 3 - Condicional con y sin sino",         test3),
        ("Test 4 - Ciclo mientras",                     test4),
        ("Test 5 - Función con parámetros y llamada",   test5),
        ("Test 6 - Flotantes y expresiones combinadas", test6),
    ]:
        print("")
        print("")
        print(f"  {nombre}")
        try:
            parser.parse(codigo, lexer=lex.lex())
            print("  Aceptado")
        except Exception as e:
            print(f"Error inesperado: {e}")

    print("\n──── CASOS INVÁLIDOS ────")
    for nombre, codigo in [
        ("E1 - ID inicia con dígito",          test_e1),
        ("E2 - Falta ':' en declaración",      test_e2),
        ("E3 - Falta paréntesis en si",        test_e3),
        ("E4 - Falta 'haz' en mientras",       test_e4),
        ("E5 - Expresión vacía en asignación", test_e5),
        ("E6 - Falta 'fin'",                   test_e6),
    ]:
        print("")
        print("")
        print(f"  {nombre}")
        try:
            parser.parse(codigo, lexer=lex.lex())
            print("  Advertencia: no se detectó error")
        except Exception as e:
            print(f"Error detectado correctamente: {e}")