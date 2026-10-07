from dataclasses import dataclass

from src.sea_complexity import SEAComplexity
from src.sea_objective import SEAOptimizationObjective


@dataclass(frozen=True)
class SEATransformation:
    source: object
    target: object
    name: str
    semantics_preserved: bool
    rationale: str = ""


@dataclass(frozen=True)
class SEAOptimizationCertificate:
    source_complexity: SEAComplexity
    target_complexity: SEAComplexity
    semantics_preserved: bool
    transformation_name: str
    objective: SEAOptimizationObjective = None
    allow_tradeoff: bool = False

    @property
    def pareto_improved(self):
        return self.target_complexity.dominates_numeric(
            self.source_complexity
        )

    @property
    def objective_result(self):
        if self.objective is None:
            return None

        return self.objective.improvement(
            self.source_complexity,
            self.target_complexity,
        )

    @property
    def objective_improved(self):
        result = self.objective_result

        if result is None:
            return False

        return result["improved"]

    @property
    def complexity_improved(self):
        if self.pareto_improved:
            return True

        if self.allow_tradeoff and self.objective_improved:
            return True

        return False

    @property
    def valid(self):
        return (
            self.semantics_preserved
            and self.complexity_improved
        )

    def summary(self):
        result = self.objective_result

        summary = {
            "transformation":
                self.transformation_name,
            "semantics_preserved":
                self.semantics_preserved,
            "pareto_improved":
                self.pareto_improved,
            "objective_improved":
                self.objective_improved,
            "tradeoff_allowed":
                self.allow_tradeoff,
            "complexity_improved":
                self.complexity_improved,
            "valid":
                self.valid,
        }

        if result is not None:
            summary.update({
                "source_score":
                    result["source_score"],
                "target_score":
                    result["target_score"],
                "objective_delta":
                    result["delta"],
            })

        return summary
