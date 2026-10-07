from dataclasses import dataclass


@dataclass(frozen=True)
class SEAOptimizationObjective:
    """
    Weighted execution objective.

    Lower score is better.

    The objective allows explicit resource trade-offs while
    preserving SEA's existing Pareto-dominance model.
    """

    time: float = 1.0
    memory: float = 0.60
    states: float = 0.75
    branching: float = 0.40
    depth: float = 0.20
    precision: float = 0.05
    interactions: float = 0.50

    def __post_init__(self):
        for name in (
            "time",
            "memory",
            "states",
            "branching",
            "depth",
            "precision",
            "interactions",
        ):
            value = getattr(self, name)

            if value < 0:
                raise ValueError(
                    f"objective weight '{name}' must be non-negative"
                )

    def score(self, complexity):
        values = complexity.numeric_tuple()

        weights = (
            self.time,
            self.memory,
            self.states,
            self.branching,
            self.depth,
            self.precision,
            self.interactions,
        )

        return sum(
            weight * value
            for weight, value in zip(weights, values)
        )

    def improvement(self, source, target):
        source_score = self.score(source)
        target_score = self.score(target)

        return {
            "source_score": source_score,
            "target_score": target_score,
            "delta": source_score - target_score,
            "improved": target_score < source_score,
        }
