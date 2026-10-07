from collections import OrderedDict


class ResultCache:
    def __init__(self, capacity=1024):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")

        self.capacity = capacity
        self._data = OrderedDict()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _freeze(value):
        if isinstance(value, dict):
            return tuple(
                sorted(
                    (key, ResultCache._freeze(item))
                    for key, item in value.items()
                )
            )

        if isinstance(value, (list, tuple)):
            return tuple(
                ResultCache._freeze(item)
                for item in value
            )

        if isinstance(value, set):
            return tuple(
                sorted(
                    ResultCache._freeze(item)
                    for item in value
                )
            )

        try:
            hash(value)
            return value
        except TypeError:
            return repr(value)

    def key(self, value):
        return self._freeze(value)

    def contains(self, value):
        key = self.key(value)

        if key not in self._data:
            self.misses += 1
            return False

        self.hits += 1
        self._data.move_to_end(key)
        return True

    def get(self, value):
        key = self.key(value)

        if key not in self._data:
            self.misses += 1
            raise KeyError(key)

        self.hits += 1
        self._data.move_to_end(key)
        return self._data[key]

    def set(self, value, result):
        key = self.key(value)
        self._data[key] = result
        self._data.move_to_end(key)

        while len(self._data) > self.capacity:
            self._data.popitem(last=False)

    def clear(self):
        self._data.clear()

    def size(self):
        return len(self._data)

    def stats(self):
        total = self.hits + self.misses

        return {
            "size": self.size(),
            "capacity": self.capacity,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": (
                self.hits / total
                if total
                else 0.0
            ),
        }
