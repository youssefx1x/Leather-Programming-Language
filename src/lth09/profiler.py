from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from time import perf_counter_ns


@dataclass
class ProfileRecord:
    operation: str
    calls: int = 0
    total_ns: int = 0

    @property
    def average_ns(self) -> float:
        if self.calls == 0:
            return 0.0
        return self.total_ns / self.calls


class HotPathProfiler:
    """Small deterministic profiler for LTH execution hot paths."""

    def __init__(self):
        self.records: dict[str, ProfileRecord] = {}

    def measure(self, operation: str, function, *args, **kwargs):
        start = perf_counter_ns()

        try:
            return function(*args, **kwargs)
        finally:
            elapsed = perf_counter_ns() - start

            record = self.records.get(operation)

            if record is None:
                record = ProfileRecord(operation)
                self.records[operation] = record

            record.calls += 1
            record.total_ns += elapsed

    def hot_paths(self):
        return sorted(
            self.records.values(),
            key=lambda item: item.total_ns,
            reverse=True,
        )

    def summary(self):
        return [
            {
                "operation": item.operation,
                "calls": item.calls,
                "total_ns": item.total_ns,
                "average_ns": item.average_ns,
            }
            for item in self.hot_paths()
        ]
