from dataclasses import dataclass

from src.sea_complexity import SEAComplexity


@dataclass(frozen=True)
class SEAComplexityProfile:
    name: str
    complexity: SEAComplexity
    problem_size: object = None

    def summary(self):
        return {
            "name": self.name,
            "problem_size": self.problem_size,
            "complexity": self.complexity.render(),
        }

    def compare(self, other):
        return {
            "this_dominates":
                self.complexity.dominates_numeric(
                    other.complexity
                ),
            "other_dominates":
                other.complexity.dominates_numeric(
                    self.complexity
                ),
        }
