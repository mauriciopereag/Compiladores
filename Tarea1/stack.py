# Stack (Pila) - LIFO (Last In, First Out)

class Stack:

    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if self.is_empty():
            print("Error: la pila esta vacia")
            return None
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            print("Error: la pila esta vacia")
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)