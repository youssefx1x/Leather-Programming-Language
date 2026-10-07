from dataclasses import dataclass

from src.optimizer.performance_model import (
    PerformanceEstimate,
)
from src.optimizer.performance_plan import (
    OptimizationCandidate,
    OptimizationPlan,
)


@dataclass(frozen=True)
class OptimizationRanking:
    candidate: OptimizationCandidate
    score: float


class PerformanceOptimizer:
    """
    Select a semantics-preserving candidate that
    strictly dominates the source cost.
    """

    def rank(self, candidates):
        return tuple(
            sorted(
                (
                    OptimizationRanking(
                        candidate=candidate,
                        score=candidate.cost.total(),
                    )
                    for candidate in candidates
                ),
                key=lambda item: (
                    item.score,
                    item.candidate.name,
                ),
            )
        )

    def optimize(
        self,
        source: PerformanceEstimate,
        candidates=(),
    ):
        compatible = tuple(
            candidate
            for candidate in candidates
            if candidate.compatible_with(source)
            and candidate.cost.dominates(source.cost)
        )

        if not compatible:
            return OptimizationPlan(
                source=source,
                selected=None,
                reason="no verified improving candidate",
            )

        selected = self.rank(
            compatible
        )[0].candidate

        return OptimizationPlan(
            source=source,
            selected=selected,
            reason="selected strict Pareto improvement",
        )
