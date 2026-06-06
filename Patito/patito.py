#Archivo principal para ejecutar pruebas del compilador Patito
# Mauricio Perea - A01571406

import lexer as lexer_module
from parser import parser
from semantica import reset_semantic, get_type
import semantica

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

test_q1 = """
programa expr_simple;
vars x, y, z : entero;
inicio
{
    x = 3 + 4 * 2;
    y = x - 1;
    z = x + y;
    escribe(z);
}
fin
"""

test_q2 = """
programa expr_relacional;
vars a, b, resultado : entero;
inicio
{
    a = 10;
    b = 5;
    resultado = a > b;
    escribe(resultado);
}
fin
"""

test_q3 = """
programa expr_flotante;
vars a, b, c : flotante;
inicio
{
    a = 1.5;
    b = 2.5;
    c = a * b + 3.0;
    escribe(c);
}
fin
"""

test_v1 = """
programa cond_virtual;
vars x : entero;
inicio
{
    x = 10;
    si (x > 5) {
        escribe("x es mayor a 5");
    };
}
fin
"""

test_v2 = """
programa ciclo_virtual;
vars i : entero;
inicio
{
    i = 0;
    mientras (i < 3) haz {
        escribe(i);
        i = i + 1;
    };
}
fin
"""

test_v3 = """
programa funcs_virtual;
nula imprime_doble (n : entero) {
    {
        escribe(n);
        escribe(n);
    }
};
inicio
{
    imprime_doble(7);
}
fin
"""

test_vm1 = """
programa aritmetica;
vars x, y, z : entero;
inicio
{
    x = 2;
    y = 3;
    z = x + y * 4;
    escribe(z);
}
fin
"""

test_vm2 = """
programa condicional;
vars x : entero;
inicio
{
    x = 8;
    si (x > 5) {
        escribe("x es mayor a 5");
    } sino {
        escribe("x es menor o igual a 5");
    }
}
fin
"""

test_vm3 = """
programa ciclo;
vars i : entero;
inicio
{
    i = 1;
    mientras (i < 6) haz {
        escribe(i);
        i = i + 1;
    };
}
fin
"""

test_vm4 = """
programa funciones;
nula doble (n : entero) {
    {
        escribe(n);
    }
};
inicio
{
    doble(10);
    doble(20);
}
fin
"""

test_vm5 = """
programa combinado;
vars i, total : entero;
nula imprime (val : entero) {
    {
        escribe(val);
    }
};
inicio
{
    total = 0;
    i = 1;
    mientras (i < 4) haz {
        total = total + i;
        i = i + 1;
    };
    imprime(total);
}
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
            parser.parse(codigo, lexer=lexer_module.get_lexer())
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
            parser.parse(codigo, lexer=lexer_module.get_lexer())
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
            parser.parse(codigo, lexer=lexer_module.get_lexer())
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

    print("\n──── CUÁDRUPLOS ────")
    for nombre, codigo in [
        ("Q1 - Expresiones aritméticas",   test_q1),
        ("Q2 - Expresión relacional",      test_q2),
        ("Q3 - Expresiones con flotantes", test_q3),
    ]:
        print("")
        print("")
        print(f"  {nombre}")
        try:
            reset_semantic()
            parser.parse(codigo, lexer=lexer_module.get_lexer())
            print("  Aceptado")
        except Exception as e:
            print(f"  Error inesperado: {e}")

    print("\n──── DIRECCIONES VIRTUALES Y CONTROL DE FLUJO ────")
    for nombre, codigo in [
        ("V1 - Condicional con direcciones virtuales", test_v1),
        ("V2 - Ciclo con direcciones virtuales",       test_v2),
        ("V3 - Función con direcciones virtuales",     test_v3),
    ]:
        print("")
        print("")
        print(f"  {nombre}")
        try:
            reset_semantic()
            parser.parse(codigo, lexer=lexer_module.get_lexer())
            print("  Aceptado")
        except Exception as e:
            print(f"  Error inesperado: {e}")
    
    print("\n──── MÁQUINA VIRTUAL ────")
    for nombre, codigo in [
        ("VM1 - Aritmética básica",  test_vm1),
        ("VM2 - Condicional",        test_vm2),
        ("VM3 - Ciclo",              test_vm3),
        ("VM4 - Función",            test_vm4),
        ("VM5 - Combinado",          test_vm5),
    ]:
        print("")
        print("")
        print(f"  {nombre}")
        try:
            reset_semantic()
            nuevo_lexer = lexer_module.get_lexer()
            parser.parse(codigo, lexer=nuevo_lexer)

            from vm import VirtualMachine
            import memoria as mem_module
            import codegen

            vm = VirtualMachine(
                cuadruplos = list(codegen.cuadruplos),
                cte_table  = dict(mem_module.cte_table),
                func_dir   = dict(semantica.func_dir),
            )
            print("  Output:")
            vm.run()
            print("  Ejecución completada ✓")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"  Error: {e}")