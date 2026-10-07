from dataclasses import dataclass
import time


@dataclass(frozen=True)
class SEABenchmarkResult:
    name: str
    elapsed_seconds: float
    result_type: str
    result_summary: str

    def summary(self):
        return {
            "name": self.name,
            "elapsed_seconds":
                self.elapsed_seconds,
            "result_type":
                self.result_type,
            "result_summary":
                self.result_summary,
        }


def benchmark(name, function):
    start = time.perf_counter()

    result = function()

    elapsed = (
        time.perf_counter()
        - start
    )

    return SEABenchmarkResult(
        name=name,
        elapsed_seconds=elapsed,
        result_type=type(result).__name__,
        result_summary=str(result),
    )


@dataclass(frozen=True)
class SEABenchmarkComparison:
    direct: SEABenchmarkResult
    symbolic: SEABenchmarkResult

    @property
    def speedup(self):
        if self.symbolic.elapsed_seconds == 0:
            return float("inf")

        return (
            self.direct.elapsed_seconds
            / self.symbolic.elapsed_seconds
        )

    def summary(self):
        return {
            "direct":
                self.direct.summary(),
            "symbolic":
                self.symbolic.summary(),
            "speedup":
                self.speedup,
        }
