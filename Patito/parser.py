import ply.yacc as yacc
from lexer import tokens
from semantica import (
    add_function, add_param, add_variable, lookup_variable,
    func_dir, current_func, print_func_dir, reset_semantic
)
from codegen import (
    emit, backpatch, generate_quadruple, print_quadruples,
    pila_operandos, pila_tipos, pila_operadores, pila_saltos, new_temp
)
from memoria import get_cte_addr
import semantica
import codegen

def p_programa(p):
    'programa : PROGRAMA prog_id PUNTOYCOMA vars_opc funcs_opc INICIO cuerpo FIN'
    emit('END', None, None, None)
    print_func_dir()
    print_quadruples()

def p_prog_id(p):
    'prog_id : ID'
    add_function(p[1], 'programa', start_quad=0)
    p[0] = p[1]

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
    result_addr = codegen.pila_operandos.pop()
    codegen.pila_tipos.pop()
    _, dest_addr = lookup_variable(p[1])
    emit('=', result_addr, None, dest_addr)

def p_condicion(p):
    'condicion : si_cond cuerpo sino_opc'

def p_si_cond(p):
    'si_cond : SI PARIZQ expresion PARDER'
    cond_addr = codegen.pila_operandos.pop()
    codegen.pila_tipos.pop()
    idx = emit('GOTOF', cond_addr, None, None)
    codegen.pila_saltos.append(idx)

def p_sino_con(p):
    'sino_opc : sino_marca cuerpo'

def p_sino_marca(p):
    'sino_marca : SINO'
    idx = emit('GOTO', None, None, None)
    gotof_idx = codegen.pila_saltos.pop()
    backpatch(gotof_idx, len(codegen.cuadruplos))
    codegen.pila_saltos.append(idx)

def p_sino_vacio(p):
    'sino_opc : PUNTOYCOMA'
    backpatch(codegen.pila_saltos.pop(), len(codegen.cuadruplos))

def p_ciclo(p):
    'ciclo : ciclo_completo'

def p_ciclo_completo(p):
    'ciclo_completo : mientras_cond HAZ cuerpo PUNTOYCOMA'
    gotof_idx = codegen.pila_saltos.pop()
    retorno   = codegen.pila_saltos.pop()
    emit('GOTO', None, None, retorno)
    backpatch(gotof_idx, len(codegen.cuadruplos))

def p_mientras_inicio(p):
    'mientras_inicio : MIENTRAS'
    codegen.pila_saltos.append(len(codegen.cuadruplos))

def p_mientras_cond(p):
    'mientras_cond : mientras_inicio PARIZQ expresion PARDER'
    cond_addr = codegen.pila_operandos.pop()
    codegen.pila_tipos.pop()
    idx = emit('GOTOF', cond_addr, None, None)
    codegen.pila_saltos.append(idx)

def p_imprime(p):
    'imprime : ESCRIBE PARIZQ imprime_items PARDER PUNTOYCOMA'

def p_imprime_items_uno(p):
    'imprime_items : imprime_item'

def p_imprime_items_mas(p):
    'imprime_items : imprime_item COMA imprime_items'

def p_imprime_item_exp(p):
    'imprime_item : expresion'
    result = codegen.pila_operandos.pop()
    codegen.pila_tipos.pop()
    emit('print', result, None, None)

def p_imprime_item_letrero(p):
    'imprime_item : LETRERO'
    emit('print', p[1], None, None)

def p_expresion_simple(p):
    'expresion : exp'
    p[0] = p[1]

def p_expresion_mayor(p):
    'expresion : exp MAYOR exp'
    codegen.pila_operadores.append('>')
    generate_quadruple('>')
    p[0] = codegen.pila_tipos[-1]

def p_expresion_menor(p):
    'expresion : exp MENOR exp'
    codegen.pila_operadores.append('<')
    generate_quadruple('<')
    p[0] = codegen.pila_tipos[-1]

def p_expresion_igual(p):
    'expresion : exp IGUAL exp'
    codegen.pila_operadores.append('==')
    generate_quadruple('==')
    p[0] = codegen.pila_tipos[-1]

def p_expresion_dif(p):
    'expresion : exp DIF exp'
    codegen.pila_operadores.append('!=')
    generate_quadruple('!=')
    p[0] = codegen.pila_tipos[-1]

def p_exp_termino(p):
    'exp : termino'
    p[0] = p[1]

def p_exp_suma(p):
    'exp : termino SUMA exp'
    codegen.pila_operadores.append('+')
    generate_quadruple('+')
    p[0] = codegen.pila_tipos[-1]

def p_exp_resta(p):
    'exp : termino RESTA exp'
    codegen.pila_operadores.append('-')
    generate_quadruple('-')
    p[0] = codegen.pila_tipos[-1]

def p_termino_factor(p):
    'termino : factor'
    p[0] = p[1]

def p_termino_mult(p):
    'termino : factor MULT termino'
    codegen.pila_operadores.append('*')
    generate_quadruple('*')
    p[0] = codegen.pila_tipos[-1]

def p_termino_div(p):
    'termino : factor DIV termino'
    codegen.pila_operadores.append('/')
    generate_quadruple('/')
    p[0] = codegen.pila_tipos[-1]

def p_factor_paren(p):
    'factor : PARIZQ expresion PARDER'
    p[0] = p[2]

def p_factor_pos(p):
    'factor : SUMA factor'
    p[0] = p[2]

def p_factor_neg(p):
    'factor : RESTA factor'
    op   = codegen.pila_operandos.pop()
    tipo = codegen.pila_tipos.pop()
    temp = new_temp(tipo)
    emit('neg', op, None, temp)
    codegen.pila_operandos.append(temp)
    codegen.pila_tipos.append(tipo)
    p[0] = tipo

def p_factor_cte_ent(p):
    'factor : CTE_ENT'
    addr = get_cte_addr(p[1], 'entero')
    codegen.pila_operandos.append(addr)
    codegen.pila_tipos.append('entero')
    p[0] = 'entero'

def p_factor_cte_flot(p):
    'factor : CTE_FLOT'
    addr = get_cte_addr(p[1], 'flotante')
    codegen.pila_operandos.append(addr)
    codegen.pila_tipos.append('flotante')
    p[0] = 'flotante'

def p_factor_id(p):
    'factor : ID'
    tipo, addr = lookup_variable(p[1])
    codegen.pila_operandos.append(addr)
    codegen.pila_tipos.append(tipo)
    p[0] = tipo

def p_factor_llamada(p):
    'factor : llamada'
    p[0] = p[1]

def p_funcs(p):
    'funcs : funcs_ret_id PARIZQ params PARDER LLAVEIZQ vars_opc cuerpo LLAVEDER PUNTOYCOMA'
    emit('ENDFUNC', None, None, None)
    semantica.current_func = list(semantica.func_dir.keys())[0]

def p_funcs_ret_id(p):
    'funcs_ret_id : tipo_ret funcs_id'
    p[0] = p[2]

def p_funcs_id(p):
    'funcs_id : ID'
    start = len(codegen.cuadruplos)
    add_function(p[1], p[-1], start_quad=start)
    semantica.func_dir[p[1]]['start_quad'] = start
    p[0] = p[1]

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
    'llamada : llamada_id PARIZQ args PARDER'
    fname = p[1]
    if fname not in semantica.func_dir:
        raise Exception(f"  Error semántico: función '{fname}' no declarada.")
    emit('GOSUB', fname, None, semantica.func_dir[fname]['start_quad'])

def p_llamada_id(p):
    'llamada_id : ID'
    emit('ERA', p[1], None, None)
    p[0] = p[1]

def p_args_vacio(p):
    'args : empty'

def p_args_uno(p):
    'args : expresion'
    arg_addr = codegen.pila_operandos.pop()
    codegen.pila_tipos.pop()
    emit('PARAM', arg_addr, None, None)

def p_args_mas(p):
    'args : expresion COMA args'
    arg_addr = codegen.pila_operandos.pop()
    codegen.pila_tipos.pop()
    emit('PARAM', arg_addr, None, None)

def p_empty(p):
    'empty :'

def p_error(p):
    if p:
        print(f"  Error de sintaxis en '{p.value}', línea {p.lineno}")
    else:
        print("  Error de sintaxis: fin de archivo inesperado")

parser = yacc.yacc()