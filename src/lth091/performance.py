from dataclasses import dataclass
import time


@dataclass
class PerformanceSnapshot:
    operation: str
    calls: int
    elapsed_ns: int

    @property
    def elapsed_ms(self):
        return self.elapsed_ns / 1_000_000

    @property
    def average_ns(self):
        if self.calls == 0:
            return 0.0
        return self.elapsed_ns / self.calls


class PerformanceTransparency:
    """
    Stable performance-observation layer.

    It observes execution without changing semantics.
    """

    def __init__(self):
        self._records = {}

    def measure(self, operation, fn, calls=1):
        start = time.perf_counter_ns()

        result = None
        for _ in range(calls):
            result = fn()

        elapsed = time.perf_counter_ns() - start

        self._records[operation] = PerformanceSnapshot(
            operation=operation,
            calls=calls,
            elapsed_ns=elapsed,
        )

        return result

    def snapshot(self, operation):
        return self._records.get(operation)

    def all(self):
        return dict(self._records)
