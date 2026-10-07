from src.execution.budget import ExecutionBudget
from src.execution.model import ExecutionWorkload
from src.execution.portfolio import (
    ExecutionStrategyPortfolio,
)
from src.execution.plan_validator import (
    ExecutionPlanValidator,
)


def main():
    workload = ExecutionWorkload(
        name="validator",
        states=100,
        branching=2,
        depth=10,
        repeated_subproblems=0.40,
    )

    _, plan = (
        ExecutionStrategyPortfolio().build(
            workload,
            budget=ExecutionBudget(
                max_memory=1000
            ),
        )
    )

    assert plan is not None
    assert ExecutionPlanValidator().validate(
        plan
    )

    print("LTH EXECUTION PLAN VALIDATOR: PASS")


if __name__ == "__main__":
    main()
