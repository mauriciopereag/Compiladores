# Hash Table (Diccionario)

class HashTable:

    def __init__(self):
        self.data = {}

    def put(self, key, value):
        self.data[key] = value

    def get(self, key):
        if key not in self.data:
            print(f"Error: la clave '{key}' no existe")
            return None
        return self.data[key]

    def remove(self, key):
        if key not in self.data:
            print(f"Error: la clave '{key}' no existe")
            return
        del self.data[key]

    def contains(self, key):
        return key in self.data

    def size(self):
        return len(self.data)

    def keys(self):
        return list(self.data.keys())

    def __str__(self):
        return str(self.data)