from dataclasses import dataclass
from time import perf_counter


@dataclass
class BenchmarkResult:
    iterations: int
    seconds: float
    nanoseconds_per_run: float


def benchmark_vm(runner, source, context=None, iterations=1000, warmup=25):
    code, _ = runner.compile(source)

    for _ in range(warmup):
        runner.vm.run(code, context=context)

    start = perf_counter()

    for _ in range(iterations):
        runner.vm.run(code, context=context)

    elapsed = perf_counter() - start

    return BenchmarkResult(
        iterations=iterations,
        seconds=elapsed,
        nanoseconds_per_run=(
            elapsed * 1_000_000_000 / iterations
        ),
    )
