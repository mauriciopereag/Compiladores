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

# ─────────────────────────────────── CUBO SEMÁNTICO ───────────────────────────

semantic_cube = {
    'entero': {
        'entero': {
            '+': 'entero',   '-': 'entero',   '*': 'entero',   '/': 'entero',
            '>': 'entero',   '<': 'entero',   '==': 'entero',  '!=': 'entero',
        },
        'flotante': {
            '+': 'flotante', '-': 'flotante', '*': 'flotante', '/': 'flotante',
            '>': 'entero',   '<': 'entero',   '==': 'entero',  '!=': 'entero',
        },
    },
    'flotante': {
        'entero': {
            '+': 'flotante', '-': 'flotante', '*': 'flotante', '/': 'flotante',
            '>': 'entero',   '<': 'entero',   '==': 'entero',  '!=': 'entero',
        },
        'flotante': {
            '+': 'flotante', '-': 'flotante', '*': 'flotante', '/': 'flotante',
            '>': 'entero',   '<': 'entero',   '==': 'entero',  '!=': 'entero',
        },
    },
}

def get_type(left, op, right):
    try:
        return semantic_cube[left][right][op]
    except KeyError:
        return 'error'

# ─────────────────────────────────── DIRECTORIO DE FUNCIONES ──────────────────

func_dir = {}
current_func = None

def add_function(name, ret_type):
    global current_func
    if name in func_dir:
        raise Exception(f"  Error semántico: función '{name}' doblemente declarada.")
    func_dir[name] = {
        'tipo': ret_type,
        'params': [],
        'vars': {}
    }
    current_func = name

def add_param(name, var_type):
    if name in func_dir[current_func]['vars']:
        raise Exception(f"  Error semántico: parámetro '{name}' doblemente declarado en '{current_func}'.")
    func_dir[current_func]['params'].append((name, var_type))
    func_dir[current_func]['vars'][name] = {'tipo': var_type}

def add_variable(name, var_type):
    scope = func_dir.get(current_func)
    if scope is None:
        raise Exception(f"  Error semántico: no hay scope activo para declarar '{name}'.")
    if name in scope['vars']:
        raise Exception(f"  Error semántico: variable '{name}' doblemente declarada en '{current_func}'.")
    scope['vars'][name] = {'tipo': var_type}

def lookup_variable(name):
    if current_func and name in func_dir[current_func]['vars']:
        return func_dir[current_func]['vars'][name]['tipo']
    if 'global' in func_dir and name in func_dir['global']['vars']:
        return func_dir['global']['vars'][name]['tipo']
    raise Exception(f"  Error semántico: variable '{name}' no declarada.")

def reset_semantic():
    global func_dir, current_func
    func_dir = {}
    current_func = None

def print_func_dir():
    print("")
    print("  Directorio de Funciones:")
    for fname, fdata in func_dir.items():
        print(f"    {fname} | tipo: {fdata['tipo']} | params: {fdata['params']}")
        for vname, vdata in fdata['vars'].items():
            print(f"      var: {vname} | tipo: {vdata['tipo']}")

# ─────────────────────────────────── PARSER ───────────────────────────────────

def p_programa(p):
    'programa : PROGRAMA ID PUNTOYCOMA vars_opc funcs_opc INICIO cuerpo FIN'
    print_func_dir()

def p_programa_nombre(p):
    'programa : PROGRAMA ID PUNTOYCOMA'
    add_function(p[2], 'programa')

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
    for var_name in p[2]:
        add_variable(var_name, p[4])

def p_lista_ids_uno(p):
    'lista_ids : ID'
    p[0] = [p[1]]

def p_lista_ids_mas(p):
    'lista_ids : ID COMA lista_ids'
    p[0] = [p[1]] + p[3]

def p_tipo_entero(p):
    'tipo : ENTERO'
    p[0] = 'entero'

def p_tipo_flotante(p):
    'tipo : FLOTANTE'
    p[0] = 'flotante'

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
    p[0] = p[1]

def p_expresion_mayor(p):
    'expresion : exp MAYOR exp'
    p[0] = get_type(p[1], '>', p[3])

def p_expresion_menor(p):
    'expresion : exp MENOR exp'
    p[0] = get_type(p[1], '<', p[3])

def p_expresion_igual(p):
    'expresion : exp IGUAL exp'
    p[0] = get_type(p[1], '==', p[3])

def p_expresion_dif(p):
    'expresion : exp DIF exp'
    p[0] = get_type(p[1], '!=', p[3])

def p_exp_termino(p):
    'exp : termino'
    p[0] = p[1]

def p_exp_suma(p):
    'exp : termino SUMA exp'
    p[0] = get_type(p[1], '+', p[3])

def p_exp_resta(p):
    'exp : termino RESTA exp'
    p[0] = get_type(p[1], '-', p[3])

def p_termino_factor(p):
    'termino : factor'
    p[0] = p[1]

def p_termino_mult(p):
    'termino : factor MULT termino'
    p[0] = get_type(p[1], '*', p[3])

def p_termino_div(p):
    'termino : factor DIV termino'
    p[0] = get_type(p[1], '/', p[3])

def p_factor_paren(p):
    'factor : PARIZQ expresion PARDER'
    p[0] = p[2]

def p_factor_pos(p):
    'factor : SUMA factor'
    p[0] = p[2]

def p_factor_neg(p):
    'factor : RESTA factor'
    p[0] = p[2]

def p_factor_cte_ent(p):
    'factor : CTE_ENT'
    p[0] = 'entero'

def p_factor_cte_flot(p):
    'factor : CTE_FLOT'
    p[0] = 'flotante'

def p_factor_id(p):
    'factor : ID'
    p[0] = lookup_variable(p[1])

def p_factor_llamada(p):
    'factor : llamada'
    p[0] = p[1]

def p_funcs(p):
    'funcs : tipo_ret ID PARIZQ params PARDER LLAVEIZQ vars_opc cuerpo LLAVEDER PUNTOYCOMA'

def p_funcs_header(p):
    'funcs_header : tipo_ret ID'
    add_function(p[2], p[1])

def p_tipo_ret_nula(p):
    'tipo_ret : NULA'
    p[0] = 'nula'

def p_tipo_ret_tipo(p):
    'tipo_ret : tipo'
    p[0] = p[1]

def p_params_vacio(p):
    'params : empty'

def p_params_uno(p):
    'params : ID DOSPUNTOS tipo'
    add_param(p[1], p[3])

def p_params_mas(p):
    'params : ID DOSPUNTOS tipo COMA params'
    add_param(p[1], p[3])

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

test_s1 = """
programa semantica;
vars x, y : entero;
vars z : flotante;
nula doble (a : entero) {
    {
        escribe(a);
    }
};
inicio
{
    x = 5;
    doble(x);
}
fin
"""

test_s2 = """
programa error_var;
vars x : entero;
vars x : flotante;
inicio
{ }
fin
"""

test_s3 = """
programa error_func;
nula foo () { { } };
nula foo () { { } };
inicio
{ }
fin
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
            reset_semantic()
            parser.parse(codigo, lexer=lex.lex())
            print("  Aceptado")
        except Exception as e:
            print(f"  Error inesperado: {e}")

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
            reset_semantic()
            parser.parse(codigo, lexer=lex.lex())
            print("  Advertencia: no se detectó error")
        except Exception as e:
            print(f"  Error detectado correctamente: {e}")

    print("\n──── CASOS SEMÁNTICOS ────")
    for nombre, codigo in [
        ("S1 - Alta correcta de variables y funciones", test_s1),
        ("S2 - Variable doblemente declarada",          test_s2),
        ("S3 - Función doblemente declarada",           test_s3),
    ]:
        print("")
        print("")
        print(f"  {nombre}")
        try:
            reset_semantic()
            parser.parse(codigo, lexer=lex.lex())
            print("  Aceptado")
        except Exception as e:
            print(f"  Error detectado correctamente: {e}")

    print("\n──── CUBO SEMÁNTICO ────")
    print("")
    casos = [
        ('entero',   '+',  'flotante'),
        ('flotante', '*',  'flotante'),
        ('entero',   '>',  'entero'),
        ('flotante', '!=', 'entero'),
        ('entero',   '/',  'entero'),
    ]
    for l, op, r in casos:
        resultado = get_type(l, op, r)
        print(f"  {l} {op} {r}  →  {resultado}")