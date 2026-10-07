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
        name="regression-search",
        kind=WorkloadKind.TREE,
        states=300,
        branching=2,
        depth=19,
        repeated_subproblems=0.75,
    )

    report = LeatherExecution().run(
        workload,
        lambda c: fibonacci_direct(19, c),
        lambda c: fibonacci_memoized(19, c),
    )

    assert report.valid
    assert report.evidence.source_result == 4181
    assert report.evidence.optimized_result == 4181
    assert (
        report.evidence.optimized_operations
        < report.evidence.source_operations
    )

    print("LEATHER EXECUTION REGRESSION: PASS")


if __name__ == "__main__":
    main()
