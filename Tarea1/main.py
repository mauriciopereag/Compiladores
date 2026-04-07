from stack import Stack
from queue import Queue
from hash_table import HashTable


# STACK
print("=== STACK ===")
s = Stack()

s.push(1)
s.push(2)
s.push(3)
print("Stack despues de 3 push:", s)
print("peek (tope):", s.peek())
print("pop:", s.pop())
print("Stack despues del pop:", s)
print("Tamano:", s.size())
print("Esta vacio?", s.is_empty())


# QUEUE
print("\n=== QUEUE ===")
q = Queue()

q.enqueue("Mauricio")
q.enqueue("Rodrigo")
q.enqueue("Vanessa")
print("Queue despues de 3 enqueue:", q)
print("front (primero):", q.front())
print("dequeue:", q.dequeue())
print("Queue despues del dequeue:", q)
print("Tamano:", q.size())
print("Esta vacia?", q.is_empty())


# HASH TABLE
print("\n=== HASH TABLE ===")
ht = HashTable()

ht.put("nombre", "Mauricio")
ht.put("edad", 21)
ht.put("carrera", "ITC")
print("Hash table:", ht)
print("get nombre:", ht.get("nombre"))
print("contains 'edad':", ht.contains("edad"))
ht.remove("carrera")
print("Despues de remove 'carrera':", ht)
print("Keys:", ht.keys())
print("Tamano:", ht.size())