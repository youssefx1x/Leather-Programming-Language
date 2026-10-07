from src.execution.engine import (
    LeatherExecutionEngine,
)
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
        name="fibonacci-search",
        kind=WorkloadKind.TREE,
        states=100,
        branching=2,
        depth=18,
        repeated_subproblems=0.70,
    )

    engine = LeatherExecutionEngine()

    result = engine.compare(
        workload=workload,
        source_function=lambda c:
            fibonacci_direct(18, c),
        optimized_function=lambda c:
            fibonacci_memoized(18, c),
    )

    assert result.decision.strategy.value == "memoized"
    assert result.evidence.output_equal
    assert result.evidence.operations_reduced
    assert result.valid

    print("LTH ADAPTIVE EXECUTION: PASS")


if __name__ == "__main__":
    main()
