from src.execution.model import (
    ExecutionWorkload,
    WorkloadKind,
)
from src.execution.selector import (
    ExecutionStrategySelector,
)


def main():
    selector = ExecutionStrategySelector()

    direct = selector.select(
        ExecutionWorkload(
            name="simple",
            kind=WorkloadKind.DIRECT,
        )
    )

    memo = selector.select(
        ExecutionWorkload(
            name="repeated",
            kind=WorkloadKind.TREE,
            states=100,
            branching=2,
            repeated_subproblems=0.60,
        )
    )

    streaming = selector.select(
        ExecutionWorkload(
            name="memory-bound",
            states=1000,
            memory_budget=100,
        )
    )

    assert direct.strategy.value == "direct"
    assert memo.strategy.value == "memoized"
    assert streaming.strategy.value == "streaming"

    print("LTH EXECUTION SELECTOR: PASS")


if __name__ == "__main__":
    main()
