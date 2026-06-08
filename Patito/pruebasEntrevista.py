import lexer as lexer_module
from parser import parser
from semantica import reset_semantic, get_type
import semantica

# ── Recursión simple: factorial recursivo ──
test_rec_simple = """
programa factorial_recursivo;
vars resultado : entero;
entero factorial (n : entero) {
    vars res : entero;
    {
        si (n < 2) {
            retorna 1;
        } sino {
            retorna n * factorial(n - 1);
        }
    }
};
inicio
{
    resultado = factorial(8);
    escribe("Factorial recursivo de 8:");
    escribe(resultado);
}
fin
"""

# ── Recursión doble: fibonacci recursivo ──
test_rec_doble = """
programa fibonacci_recursivo;
vars resultado : entero;
entero fibonacci (n : entero) {
    {
        si (n < 2) {
            retorna n;
        } sino {
            retorna fibonacci(n - 1) + fibonacci(n - 2);
        }
    }
};
inicio
{
    resultado = fibonacci(7);
    escribe("Fibonacci recursivo fib(7):");
    escribe(resultado);
}
fin
"""

if __name__ == "__main__":
    print("\n──── RECURSIÓN ────")
    for nombre, codigo in [
        ("R1 - Factorial recursivo (recursión simple)", test_rec_simple),
        ("R2 - Fibonacci recursivo (recursión doble)", test_rec_doble),
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