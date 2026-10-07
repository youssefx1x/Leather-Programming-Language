class ExecutionMemo:
    def __init__(self):
        self._values = {}

    def get(self, key):
        return self._values[key]

    def contains(self, key):
        return key in self._values

    def set(self, key, value):
        self._values[key] = value

    def clear(self):
        self._values.clear()

    def size(self):
        return len(self._values)
