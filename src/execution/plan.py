from dataclasses import dataclass

from src.execution.strategy import ExecutionStrategy


@dataclass(frozen=True)
class ExecutionPlan:
    strategy: ExecutionStrategy
    reason: str
    confidence: float
    estimated_cost: object
    budget_ok: bool
    cache_enabled: bool = False

    @property
    def valid(self):
        return (
            0.0 <= self.confidence <= 1.0
            and self.budget_ok
        )

    def describe(self):
        return {
            "strategy": self.strategy.value,
            "reason": self.reason,
            "confidence": self.confidence,
            "estimated_cost": self.estimated_cost.render(),
            "budget_ok": self.budget_ok,
            "cache_enabled": self.cache_enabled,
            "valid": self.valid,
        }
