from src.execution.controller import (
    AdaptiveExecutionController,
)
from src.execution.model import (
    ExecutionWorkload,
    WorkloadKind,
)
from src.execution.budget import (
    ExecutionBudget,
)
from src.execution.search_workload import (
    fibonacci_direct,
    fibonacci_memoized,
)


def main():
    workload = ExecutionWorkload(
        name="regression-0.2",
        kind=WorkloadKind.SEARCH,
        states=500,
        branching=2,
        depth=22,
        repeated_subproblems=0.90,
    )

    result = AdaptiveExecutionController().run(
        workload=workload,
        source_function=lambda c:
            fibonacci_direct(22, c),
        optimized_function=lambda c:
            fibonacci_memoized(22, c),
        budget=ExecutionBudget(
            max_memory=1000,
            max_states=500,
            max_depth=30,
        ),
    )

    assert result.valid
    assert result.benchmark.source_result == 17711
    assert result.benchmark.optimized_result == 17711
    assert (
        result.benchmark.optimized_operations
        < result.benchmark.source_operations
    )

    print("LEATHER EXECUTION 0.2 REGRESSION: PASS")


if __name__ == "__main__":
    main()
