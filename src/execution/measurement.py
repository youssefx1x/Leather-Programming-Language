from dataclasses import dataclass
from time import perf_counter_ns


@dataclass(frozen=True)
class ExecutionMeasurement:
    result: object
    elapsed_ns: int
    operations: int
    states: int
    branches: int
    cache_hits: int
    cache_misses: int

    @property
    def seconds(self):
        return self.elapsed_ns / 1_000_000_000

    @property
    def cache_hit_rate(self):
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total


class ExecutionMeasurer:
    def measure(self, function, counter):
        started = perf_counter_ns()
        result = function(counter)
        elapsed = perf_counter_ns() - started

        return ExecutionMeasurement(
            result=result,
            elapsed_ns=elapsed,
            operations=counter.operations,
            states=counter.states,
            branches=counter.branches,
            cache_hits=counter.cache_hits,
            cache_misses=counter.cache_misses,
        )
