from src.execution.budget import ExecutionBudget
from src.optimizer.performance_model import PerformanceCost


def main():
    budget = ExecutionBudget(
        max_time=100,
        max_memory=100,
        max_states=100,
        max_operations=100,
        max_depth=20,
    )

    good = PerformanceCost(
        time=50,
        memory=80,
        states=70,
        branching=5,
        depth=10,
        precision=1,
        interactions=60,
    )

    bad = PerformanceCost(
        time=150,
        memory=80,
        states=70,
        branching=5,
        depth=10,
        precision=1,
        interactions=60,
    )

    assert budget.fits(good)
    assert not budget.fits(bad)
    assert budget.violations(bad)[0]["dimension"] == "time"

    print("LTH EXECUTION BUDGET: PASS")


if __name__ == "__main__":
    main()
