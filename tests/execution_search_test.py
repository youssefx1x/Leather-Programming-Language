from src.execution.counter import ExecutionCounter
from src.execution.search_workload import (
    fibonacci_direct,
    fibonacci_memoized,
)


def main():
    direct_counter = ExecutionCounter()
    memo_counter = ExecutionCounter()

    direct_result = fibonacci_direct(
        18,
        direct_counter,
    )

    memo_result = fibonacci_memoized(
        18,
        memo_counter,
    )

    assert direct_result == 2584
    assert memo_result == 2584

    assert memo_counter.operations < direct_counter.operations
    assert memo_counter.cache_hits > 0

    print("LTH EXECUTION SEARCH: PASS")


if __name__ == "__main__":
    main()
