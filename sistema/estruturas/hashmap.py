class Hashmap:
    def __init__(self):
        self.map = [[] for i in range(10)]
        self.collisions = 0

    def str_to_int(self, text):
        result = 0
        for c in text:
            result = result * 7 + ord(c)
        return result

    def insert(self, key, val):
        if isinstance(key, str):
            int_key = self.str_to_int(key)
        else:
            int_key = key
        index = int_key % 10
        for i, (k, _) in enumerate(self.map[index]):
            if k == key:
                self.map[index][i] = (key, val)
                return
        if self.map[index]:
            self.collisions += 1
        self.map[index].append((key, val))

    def get_val(self, key):
        if isinstance(key, str):
            int_key = self.str_to_int(key)
        else:
            int_key = key
        index = int_key % 10
        for k, v in self.map[index]:
            if key == k:
                return v
        return None