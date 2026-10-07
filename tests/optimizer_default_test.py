from src.semantic.unified_planner import UnifiedExecutionPlan
from src.optimizer.adaptive_optimizer import AdaptiveOptimizer


def test_optimizer_without_constraints():
    plan = UnifiedExecutionPlan()

    plan.add(
        "DEFINE",
        "price",
        value_kind="number",
        value=150.5,
    )

    plan.add(
        "FLOW",
        "backup",
        steps=(
            "collect",
            "compress",
            "encrypt",
            "upload",
        ),
    )

    optimized = AdaptiveOptimizer().optimize(
        plan
    )

    assert len(optimized.report.decisions) == 0

    assert "optimization" not in (
        plan.steps[1].details
    )

    print(optimized.report.describe())
    print()
    print("OPTIMIZER DEFAULT TEST PASSED")


if __name__ == "__main__":
    test_optimizer_without_constraints()
