from dataclasses import dataclass
from time import perf_counter_ns


@dataclass(frozen=True)
class RuntimeMeasurement:
    result: object
    elapsed_ns: int

    @property
    def seconds(self):
        return self.elapsed_ns / 1_000_000_000


class PerformanceRuntime:
    def measure(self, function, *args, **kwargs):
        started = perf_counter_ns()

        result = function(
            *args,
            **kwargs,
        )

        elapsed = perf_counter_ns() - started

        return RuntimeMeasurement(
            result=result,
            elapsed_ns=elapsed,
        )
