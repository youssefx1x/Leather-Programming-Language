from src.execution.benchmark import (
    ExecutionBenchmark,
)
from src.execution.search_workload import (
    fibonacci_direct,
    fibonacci_memoized,
)


def main():
    benchmark = ExecutionBenchmark()

    result = benchmark.compare(
        source_function=lambda c:
            fibonacci_direct(18, c),
        optimized_function=lambda c:
            fibonacci_memoized(18, c),
    )

    assert result.output_equal
    assert result.operations_saved > 0
    assert result.operation_reduction_ratio > 0.0
    assert result.valid

    print("LTH EXECUTION BENCHMARK: PASS")


if __name__ == "__main__":
    main()
