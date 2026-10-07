from dataclasses import dataclass


@dataclass
class ExecutionCounter:
    operations: int = 0
    states: int = 0
    branches: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

    def operation(self, amount=1):
        self.operations += amount

    def state(self, amount=1):
        self.states += amount

    def branch(self, amount=1):
        self.branches += amount

    def hit(self):
        self.cache_hits += 1

    def miss(self):
        self.cache_misses += 1

    def snapshot(self):
        return {
            "operations": self.operations,
            "states": self.states,
            "branches": self.branches,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
        }
