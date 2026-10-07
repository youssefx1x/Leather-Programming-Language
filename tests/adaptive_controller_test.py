from src.execution.budget import ExecutionBudget
from src.execution.controller import (
    AdaptiveExecutionController,
)
from src.execution.model import (
    ExecutionWorkload,
    WorkloadKind,
)
from src.execution.search_workload import (
    fibonacci_direct,
    fibonacci_memoized,
)
from src.semantic.execution_intent import (
    ExecutionIntent,
)


def main():
    workload = ExecutionWorkload(
        name="adaptive-fibonacci",
        kind=WorkloadKind.SEARCH,
        states=300,
        branching=2,
        depth=20,
        repeated_subproblems=0.80,
    )

    result = AdaptiveExecutionController().run(
        workload=workload,
        source_function=lambda c:
            fibonacci_direct(20, c),
        optimized_function=lambda c:
            fibonacci_memoized(20, c),
        intent=ExecutionIntent(
            target="adaptive",
            preserve_semantics=True,
        ),
        budget=ExecutionBudget(
            max_memory=1000,
            max_states=300,
        ),
    )

    assert result.plan.valid
    assert result.benchmark.valid
    assert result.sea_certificate.valid
    assert result.valid

    print("LTH ADAPTIVE CONTROLLER: PASS")


if __name__ == "__main__":
    main()
