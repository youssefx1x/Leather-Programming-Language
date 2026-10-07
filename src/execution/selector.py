from src.execution.model import ExecutionWorkload
from src.execution.strategy import (
    ExecutionDecision,
    ExecutionStrategy,
)


class ExecutionStrategySelector:
    def select(self, workload: ExecutionWorkload):
        if (
            workload.memory_budget is not None
            and workload.states > workload.memory_budget
        ):
            return ExecutionDecision(
                strategy=ExecutionStrategy.STREAMING,
                reason="state population exceeds memory budget",
                confidence=0.90,
            )

        if workload.repeated_subproblems >= 0.20:
            return ExecutionDecision(
                strategy=ExecutionStrategy.MEMOIZED,
                reason="repeated subproblems justify memoization",
                confidence=min(
                    0.99,
                    0.60 + workload.repeated_subproblems,
                ),
            )

        if (
            workload.kind.value in {"search", "tree", "graph"}
            and workload.states >= 100
            and workload.branching >= 4
        ):
            return ExecutionDecision(
                strategy=ExecutionStrategy.SHARED_STATE,
                reason="large branching workload benefits from shared state",
                confidence=0.85,
            )

        return ExecutionDecision(
            strategy=ExecutionStrategy.DIRECT,
            reason="no stronger strategy signal detected",
            confidence=0.75,
        )
