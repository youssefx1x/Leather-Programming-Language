from src.execution.budget import ExecutionBudget
from src.execution.model import (
    ExecutionWorkload,
    WorkloadKind,
)
from src.execution.portfolio import (
    ExecutionStrategyPortfolio,
)
from src.semantic.execution_intent import (
    ExecutionIntent,
)


def main():
    workload = ExecutionWorkload(
        name="portfolio-search",
        kind=WorkloadKind.TREE,
        states=500,
        branching=3,
        depth=20,
        repeated_subproblems=0.70,
        memory_budget=1000,
    )

    portfolio = ExecutionStrategyPortfolio()

    result, plan = portfolio.build(
        workload,
        budget=ExecutionBudget(
            max_memory=1000,
            max_states=500,
        ),
        intent=ExecutionIntent(),
    )

    assert result.valid
    assert plan is not None
    assert plan.valid
    assert plan.strategy.value in {
        "memoized",
        "shared_state",
        "direct",
        "streaming",
    }

    print("LTH STRATEGY PORTFOLIO: PASS")


if __name__ == "__main__":
    main()
