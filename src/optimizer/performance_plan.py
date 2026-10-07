from dataclasses import dataclass

from src.optimizer.performance_model import PerformanceCost


@dataclass(frozen=True)
class OptimizationCandidate:
    name: str
    cost: PerformanceCost
    meaning_signature: str
    semantics_preserved: bool = True
    rationale: str = ""

    def compatible_with(self, source):
        return (
            self.meaning_signature
            == source.meaning_signature
            and self.semantics_preserved
        )


@dataclass(frozen=True)
class OptimizationPlan:
    source: object
    selected: object = None
    reason: str = ""

    @property
    def improved(self):
        if self.selected is None:
            return False

        return self.selected.cost.dominates(
            self.source.cost
        )

    @property
    def valid(self):
        if self.selected is None:
            return True

        return (
            self.selected.compatible_with(self.source)
            and self.improved
        )

    def summary(self):
        return {
            "source": self.source.name,
            "selected": (
                self.selected.name
                if self.selected is not None
                else None
            ),
            "improved": self.improved,
            "valid": self.valid,
            "reason": self.reason,
        }
