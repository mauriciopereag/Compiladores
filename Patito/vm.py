import semantica
import codegen
import memoria as mem_module

class VirtualMachine:

    def __init__(self, cuadruplos, cte_table, func_dir):
        self.cuadruplos   = cuadruplos
        self.func_dir     = func_dir
        self.memoria      = {}
        self.call_stack   = []
        self.ret_stack    = []
        self.param_buffer = []
        self.current_era  = None

        for value, addr in cte_table.items():
            self.memoria[addr] = value

    def read(self, addr):
        if addr is None:
            return None
        if self.call_stack and addr in self.call_stack[-1]:
            return self.call_stack[-1][addr]
        return self.memoria.get(addr, 0)

    def write(self, addr, value):
        if self.call_stack and 3000 <= addr <= 4999:
            self.call_stack[-1][addr] = value
        else:
            self.memoria[addr] = value

    def run(self):
        ip = 0
        while ip < len(self.cuadruplos):
            op, left, right, result = self.cuadruplos[ip]

            if op == 'END':
                break

            elif op == '=':
                self.write(result, self.read(left))
                ip += 1

            elif op == '+':
                self.write(result, self.read(left) + self.read(right))
                ip += 1

            elif op == '-':
                self.write(result, self.read(left) - self.read(right))
                ip += 1

            elif op == '*':
                self.write(result, self.read(left) * self.read(right))
                ip += 1

            elif op == '/':
                divisor = self.read(right)
                if divisor == 0:
                    raise Exception("  Error en tiempo de ejecución: división entre cero.")
                self.write(result, self.read(left) / divisor)
                ip += 1

            elif op == '>':
                self.write(result, int(self.read(left) > self.read(right)))
                ip += 1

            elif op == '<':
                self.write(result, int(self.read(left) < self.read(right)))
                ip += 1

            elif op == '==':
                self.write(result, int(self.read(left) == self.read(right)))
                ip += 1

            elif op == '!=':
                self.write(result, int(self.read(left) != self.read(right)))
                ip += 1

            elif op == 'neg':
                self.write(result, -self.read(left))
                ip += 1

            elif op == 'print':
                if isinstance(left, str) and left.startswith('"'):
                    print(left[1:-1])
                else:
                    print(self.read(left))
                ip += 1

            elif op == 'GOTO':
                ip = result

            elif op == 'GOTOF':
                if not self.read(left):
                    ip = result
                else:
                    ip += 1

            elif op == 'ERA':
                self.current_era = left
                ip += 1

            elif op == 'PARAM':
                self.param_buffer.append(self.read(left))
                ip += 1

            elif op == 'GOSUB':
                fname     = left
                local_ctx = {}
                params    = self.func_dir[fname]['params']
                for i, (pname, ptype, paddr) in enumerate(params):
                    if i < len(self.param_buffer):
                        local_ctx[paddr] = self.param_buffer[i]
                self.param_buffer = []
                self.call_stack.append(local_ctx)
                self.ret_stack.append(ip + 1)
                ip = result

            elif op == 'ENDFUNC':
                self.call_stack.pop()
                ip = self.ret_stack.pop()

            else:
                raise Exception(f"  Código de operación desconocido: '{op}'")