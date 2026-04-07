# Casos de prueba para Stack, Queue y Hash Table

from stack import Stack
from queue import Queue
from hash_table import HashTable


def test_stack():
    print("Test Stack")
    s = Stack()

    # push
    s.push(5)
    assert s.size() == 1, "Fallo: push no agrego el elemento"
    print("push: OK")

    # peek
    assert s.peek() == 5, "Fallo: peek no retorna el tope correcto"
    print("peek: OK")

    # pop
    valor = s.pop()
    assert valor == 5, "Fallo: pop no retorno el valor correcto"
    print("pop: OK")

    # is_empty
    assert s.is_empty() == True, "Fallo: la pila deberia estar vacia"
    print("is_empty: OK")

    # size
    s.push(1)
    s.push(2)
    assert s.size() == 2, "Fallo: size incorrecto"
    print("size: OK")


def test_queue():
    print("\nTest Queue")
    q = Queue()

    # enqueue
    q.enqueue("A")
    assert q.size() == 1, "Fallo: enqueue no agrego el elemento"
    print("enqueue: OK")

    # front
    assert q.front() == "A", "Fallo: front no retorna el primero"
    print("front: OK")

    # dequeue
    valor = q.dequeue()
    assert valor == "A", "Fallo: dequeue no retorno el valor correcto"
    print("dequeue: OK")

    # is_empty
    assert q.is_empty() == True, "Fallo: la cola deberia estar vacia"
    print("is_empty: OK")

    # size
    q.enqueue("X")
    q.enqueue("Y")
    assert q.size() == 2, "Fallo: size incorrecto"
    print("size: OK")


def test_hash_table():
    print("\nTest Hash Table")
    ht = HashTable()

    # put
    ht.put("clave", 99)
    assert ht.size() == 1, "Fallo: put no agrego la entrada"
    print("put: OK")

    # get
    assert ht.get("clave") == 99, "Fallo: get no retorna el valor correcto"
    print("get: OK")

    # contains
    assert ht.contains("clave") == True, "Fallo: contains deberia retornar True"
    print("contains: OK")

    # remove
    ht.remove("clave")
    assert ht.contains("clave") == False, "Fallo: la clave deberia haberse eliminado"
    print("remove: OK")

    # keys
    ht.put("a", 1)
    ht.put("b", 2)
    assert "a" in ht.keys() and "b" in ht.keys(), "Fallo: keys no incluye todas las claves"
    print("keys: OK")

    # size
    assert ht.size() == 2, "Fallo: size incorrecto"
    print("size: OK")


# llamada a ejecutar todos los tests
test_stack()
test_queue()
test_hash_table()

print("\nTodos los tests pasaron!")