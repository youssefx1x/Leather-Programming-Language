from dataclasses import dataclass
from enum import Enum


class SEADominance(Enum):
    BETTER = "better"
    WORSE = "worse"
    EQUAL = "equal"
    INCOMPARABLE = "incomparable"


@dataclass(frozen=True)
class SEAMetricVector:
    values: tuple

    def __post_init__(self):
        if not self.values:
            raise ValueError(
                "metric vector cannot be empty"
            )

    @property
    def dimension(self):
        return len(self.values)


def _dominates(left, right):
    not_worse = all(
        a <= b
        for a, b in zip(left, right)
    )

    strictly_better = any(
        a < b
        for a, b in zip(left, right)
    )

    return not_worse and strictly_better


def pareto_compare(left, right):
    left = tuple(left)
    right = tuple(right)

    if len(left) != len(right):
        raise ValueError(
            "vectors must have equal dimensions"
        )

    left_better = _dominates(
        left,
        right,
    )

    right_better = _dominates(
        right,
        left,
    )

    if left_better:
        return SEADominance.BETTER

    if right_better:
        return SEADominance.WORSE

    if left == right:
        return SEADominance.EQUAL

    return SEADominance.INCOMPARABLE


@dataclass(frozen=True)
class SEAParetoPoint:
    name: str
    metrics: SEAMetricVector


@dataclass(frozen=True)
class SEAParetoFrontier:
    points: tuple

    def nondominated(self):
        result = []

        for candidate in self.points:
            dominated = False

            for other in self.points:
                if candidate == other:
                    continue

                if (
                    pareto_compare(
                        other.metrics.values,
                        candidate.metrics.values,
                    )
                    == SEADominance.BETTER
                ):
                    dominated = True
                    break

            if not dominated:
                result.append(candidate)

        return tuple(result)
