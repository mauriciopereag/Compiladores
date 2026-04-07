# Queue (Cola) - FIFO (First In, First Out)

class Queue:

    def __init__(self):
        self.data = []

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        if self.is_empty():
            print("Error: la cola esta vacia")
            return None
        return self.data.pop(0)

    def front(self):
        if self.is_empty():
            print("Error: la cola esta vacia")
            return None
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)