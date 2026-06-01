from memoria import next_addr, reset_addresses
from codegen import reset_codegen

func_dir     = {}
current_func = None

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

def add_function(name, ret_type, start_quad=None):
    global current_func
    if name in func_dir:
        raise Exception(f"  Error semántico: función '{name}' doblemente declarada.")
    func_dir[name] = {'tipo': ret_type, 'params': [], 'vars': {}, 'start_quad': start_quad}
    current_func = name

def add_param(name, var_type):
    if name in func_dir[current_func]['vars']:
        raise Exception(f"  Error semántico: parámetro '{name}' doblemente declarado en '{current_func}'.")
    addr = next_addr('local', var_type)
    func_dir[current_func]['params'].append((name, var_type, addr))
    func_dir[current_func]['vars'][name] = {'tipo': var_type, 'addr': addr}

def add_variable(name, var_type):
    scope = func_dir.get(current_func)
    if scope is None:
        raise Exception(f"  Error semántico: no hay scope activo para declarar '{name}'.")
    if name in scope['vars']:
        raise Exception(f"  Error semántico: variable '{name}' doblemente declarada en '{current_func}'.")
    seg  = 'global' if current_func == list(func_dir.keys())[0] else 'local'
    addr = next_addr(seg, var_type)
    scope['vars'][name] = {'tipo': var_type, 'addr': addr}

def lookup_variable(name):
    if current_func and name in func_dir[current_func]['vars']:
        v = func_dir[current_func]['vars'][name]
        return v['tipo'], v['addr']
    first = list(func_dir.keys())[0]
    if first in func_dir and name in func_dir[first]['vars']:
        v = func_dir[first]['vars'][name]
        return v['tipo'], v['addr']
    raise Exception(f"  Error semántico: variable '{name}' no declarada.")

def reset_semantic():
    global func_dir, current_func
    func_dir     = {}
    current_func = None
    reset_codegen()
    reset_addresses()

def print_func_dir():
    print("")
    print("  Directorio de Funciones:")
    for fname, fdata in func_dir.items():
        print(f"    {fname} | tipo: {fdata['tipo']} | start: {fdata['start_quad']} | params: {[(p[0],p[1],p[2]) for p in fdata['params']]}")
        for vname, vdata in fdata['vars'].items():
            print(f"      var: {vname} | tipo: {vdata['tipo']} | addr: {vdata['addr']}")