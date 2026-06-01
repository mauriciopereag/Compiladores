from memoria import next_addr

pila_operandos  = []
pila_operadores = []
pila_tipos      = []
pila_saltos     = []
cuadruplos      = []

def new_temp(tipo):
    return next_addr('temp', tipo)

def reset_codegen():
    global pila_operandos, pila_operadores, pila_tipos, pila_saltos, cuadruplos
    pila_operandos  = []
    pila_operadores = []
    pila_tipos      = []
    pila_saltos     = []
    cuadruplos      = []

def emit(op, left, right, result):
    cuadruplos.append((op, left, right, result))
    return len(cuadruplos) - 1

def backpatch(quad_idx, value):
    q = cuadruplos[quad_idx]
    cuadruplos[quad_idx] = (q[0], q[1], q[2], value)

def generate_quadruple(op):
    from semantica import get_type

    right_op   = pila_operandos.pop()
    right_type = pila_tipos.pop()
    left_op    = pila_operandos.pop()
    left_type  = pila_tipos.pop()
    pila_operadores.pop()
    result_type = get_type(left_type, op, right_type)
    if result_type == 'error':
        raise Exception(f"  Error semántico: operación '{left_type} {op} {right_type}' no permitida.")
    temp = new_temp(result_type)
    emit(op, left_op, right_op, temp)
    pila_operandos.append(temp)
    pila_tipos.append(result_type)

def print_quadruples():
    print("")
    print("  Cuádruplos generados:")
    for i, q in enumerate(cuadruplos):
        print(f"    {i:>3}:  {str(q[0]):<10}  {str(q[1]):<10}  {str(q[2]):<10}  {str(q[3])}")