from src.leather_execution import LeatherExecution
from src.execution.model import (
    ExecutionWorkload,
    WorkloadKind,
)
from src.execution.search_workload import (
    fibonacci_direct,
    fibonacci_memoized,
)


def main():
    workload = ExecutionWorkload(
        name="core-search-workload",
        kind=WorkloadKind.SEARCH,
        states=250,
        branching=2,
        depth=20,
        repeated_subproblems=0.80,
    )

    report = LeatherExecution().run(
        workload=workload,
        source_function=lambda c:
            fibonacci_direct(20, c),
        optimized_function=lambda c:
            fibonacci_memoized(20, c),
    )

    assert report.decision.strategy.value == "memoized"
    assert report.evidence.output_equal
    assert report.evidence.operations_reduced
    assert report.valid

    print("LEATHER EXECUTION INTEGRATION: PASS")


if __name__ == "__main__":
    main()
