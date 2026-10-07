from src.execution.plan import ExecutionPlan
from src.execution.strategy import ExecutionStrategy


class ExecutionPlanValidator:
    VALID_STRATEGIES = frozenset(
        ExecutionStrategy
    )

    def validate(self, plan):
        if not isinstance(plan, ExecutionPlan):
            return False

        if plan.strategy not in self.VALID_STRATEGIES:
            return False

        if not 0.0 <= plan.confidence <= 1.0:
            return False

        if not plan.budget_ok:
            return False

        return bool(plan.valid)
