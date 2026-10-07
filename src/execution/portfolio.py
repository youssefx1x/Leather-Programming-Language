from dataclasses import dataclass

from src.execution.budget import ExecutionBudget
from src.execution.cache_policy import CachePolicy
from src.execution.model import ExecutionWorkload
from src.execution.plan import ExecutionPlan
from src.execution.plan_validator import ExecutionPlanValidator
from src.execution.strategy import ExecutionStrategy


@dataclass(frozen=True)
class StrategyCandidate:
    strategy: ExecutionStrategy
    cost: object
    score: float
    reason: str


@dataclass(frozen=True)
class StrategyPortfolio:
    candidates: tuple
    selected: StrategyCandidate | None

    @property
    def valid(self):
        return (
            self.selected is not None
            and self.selected.strategy
            in tuple(ExecutionStrategy)
        )

    def describe(self):
        return {
            "candidates": tuple(
                {
                    "strategy": item.strategy.value,
                    "score": item.score,
                    "reason": item.reason,
                    "cost": item.cost.render(),
                }
                for item in self.candidates
            ),
            "selected": (
                self.selected.strategy.value
                if self.selected
                else None
            ),
            "valid": self.valid,
        }


class ExecutionStrategyPortfolio:
    def __init__(self):
        self.cache_policy = CachePolicy()
        self.validator = ExecutionPlanValidator()

    def _score(self, cost):
        return (
            cost.time
            + cost.memory * 0.60
            + cost.states * 0.75
            + cost.branching * 0.40
            + cost.depth * 0.20
            + cost.precision * 0.05
            + cost.interactions * 0.50
        )

    def build(
        self,
        workload: ExecutionWorkload,
        budget: ExecutionBudget | None = None,
        intent=None,
    ):
        budget = budget or ExecutionBudget()

        strategy_names = (
            ExecutionStrategy.DIRECT,
            ExecutionStrategy.MEMOIZED,
            ExecutionStrategy.SHARED_STATE,
            ExecutionStrategy.STREAMING,
        )

        candidates = []

        cache = self.cache_policy.decide(
            repeated_subproblems=workload.repeated_subproblems,
            states=workload.states,
            memory_budget=workload.memory_budget,
        )

        for strategy in strategy_names:
            strategy_name = strategy.value

            if intent is not None:
                if not intent.permits(strategy_name):
                    continue

            if (
                strategy == ExecutionStrategy.MEMOIZED
                and not cache.enabled
            ):
                continue

            cost = workload.strategy_cost(
                strategy_name
            )

            if not budget.fits(cost):
                continue

            reason = (
                "baseline strategy"
                if strategy == ExecutionStrategy.DIRECT
                else "predicted lower-cost execution"
            )

            candidates.append(
                StrategyCandidate(
                    strategy=strategy,
                    cost=cost,
                    score=self._score(cost),
                    reason=reason,
                )
            )

        candidates.sort(
            key=lambda item: (
                item.score,
                item.strategy.value,
            )
        )

        selected = (
            candidates[0]
            if candidates
            else None
        )

        portfolio = StrategyPortfolio(
            candidates=tuple(candidates),
            selected=selected,
        )

        if not portfolio.valid:
            return portfolio, None

        plan = ExecutionPlan(
            strategy=selected.strategy,
            reason=selected.reason,
            confidence=0.90,
            estimated_cost=selected.cost,
            budget_ok=budget.fits(
                selected.cost
            ),
            cache_enabled=(
                selected.strategy
                == ExecutionStrategy.MEMOIZED
                and cache.enabled
            ),
        )

        if not self.validator.validate(plan):
            raise ValueError(
                "invalid execution plan generated"
            )

        return portfolio, plan
