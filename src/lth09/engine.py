from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any


@dataclass
class ExecutionStats:
    calls: int = 0
    fast_path_hits: int = 0
    cache_hits: int = 0
    cache_misses: int = 0

    @property
    def fast_path_rate(self) -> float:
        if self.calls == 0:
            return 0.0
        return self.fast_path_hits / self.calls


class AcceleratedEngine:
    """
    LTH 0.9 semantic-preserving execution engine.

    The engine accelerates only operations whose canonical
    semantics are already established by LTH 0.8.
    """

    def __init__(self, cache_size: int = 4096):
        self.stats = ExecutionStats()
        self._cache_size = cache_size

        @lru_cache(maxsize=cache_size)
        def cached_add(left: Any, right: Any):
            return self._semantic_add(left, right)

        self._cached_add = cached_add

    @staticmethod
    def _semantic_add(left: Any, right: Any):
        if isinstance(left, str) and isinstance(right, str):
            return left + right

        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return left + right

        raise TypeError("unsupported add")

    def add(self, left: Any, right: Any):
        self.stats.calls += 1

        if (
            isinstance(left, int)
            and not isinstance(left, bool)
            and isinstance(right, int)
            and not isinstance(right, bool)
        ):
            self.stats.fast_path_hits += 1
            self.stats.cache_misses += 1
            return left + right

        if isinstance(left, str) and isinstance(right, str):
            self.stats.fast_path_hits += 1
            self.stats.cache_misses += 1
            return left + right

        before = self._cached_add.cache_info().hits
        result = self._cached_add(left, right)
        after = self._cached_add.cache_info().hits

        if after > before:
            self.stats.cache_hits += 1
        else:
            self.stats.cache_misses += 1

        return result

    def reset_stats(self):
        self.stats = ExecutionStats()
        self._cached_add.cache_clear()

    def cache_info(self):
        return self._cached_add.cache_info()
