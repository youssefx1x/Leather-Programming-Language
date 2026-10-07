from dataclasses import dataclass

from src.optimizer.performance_model import (
    PerformanceCost,
)


@dataclass(frozen=True)
class PerformanceEvidence:
    name: str
    source_output: object
    target_output: object
    source_cost: PerformanceCost
    target_cost: PerformanceCost
    semantics_preserved: bool
    measured_elapsed_ns: int = 0

    @property
    def output_equal(self):
        return (
            self.source_output
            == self.target_output
        )

    @property
    def resource_improved(self):
        return self.target_cost.dominates(
            self.source_cost
        )

    @property
    def valid(self):
        return (
            self.output_equal
            and self.semantics_preserved
            and self.resource_improved
        )

    def summary(self):
        return {
            "name": self.name,
            "output_equal": self.output_equal,
            "semantics_preserved":
                self.semantics_preserved,
            "resource_improved":
                self.resource_improved,
            "valid": self.valid,
            "measured_elapsed_ns":
                self.measured_elapsed_ns,
        }
