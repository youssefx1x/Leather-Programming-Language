from collections import OrderedDict


class CompilationCache:
    def __init__(self, max_entries=64):
        self.max_entries = max_entries
        self._items = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key not in self._items:
            self.misses += 1
            return None

        self.hits += 1
        value = self._items.pop(key)
        self._items[key] = value
        return value

    def put(self, key, value):
        if key in self._items:
            self._items.pop(key)

        self._items[key] = value

        while len(self._items) > self.max_entries:
            self._items.popitem(last=False)

        return value

    def clear(self):
        self._items.clear()
        self.hits = 0
        self.misses = 0

    def __len__(self):
        return len(self._items)
