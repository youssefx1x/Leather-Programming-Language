from dataclasses import dataclass
import math

from src.sea_complexity import ComplexityExpr
from src.sea_huge import SEAHugeNumber


def _expr(value):
    if isinstance(value, ComplexityExpr):
        return value
    return ComplexityExpr.const(value)


@dataclass(frozen=True)
class SEASearchSpace:
    branching: object
    depth: object

    def _evaluated_parameters(self, environment=None):
        environment = environment or {}

        branching = _expr(
            self.branching
        ).evaluate(environment)

        depth = _expr(
            self.depth
        ).evaluate(environment)

        if branching < 0:
            raise ValueError(
                "branching must be non-negative"
            )

        if depth < 0 or int(depth) != depth:
            raise ValueError(
                "depth must be a non-negative integer"
            )

        if int(branching) != branching:
            raise ValueError(
                "branching must be an integer"
            )

        return int(branching), int(depth)

    def frontier(self, environment=None):
        branching, depth = (
            self._evaluated_parameters(environment)
        )

        return branching ** depth

    def total_nodes(self, environment=None):
        branching, depth = (
            self._evaluated_parameters(environment)
        )

        if branching == 0:
            return 1

        if branching == 1:
            return depth + 1

        return (
            branching ** (depth + 1) - 1
        ) // (branching - 1)

    def huge_total_nodes(self, environment=None):
        branching, depth = (
            self._evaluated_parameters(environment)
        )

        if branching <= 1:
            return SEAHugeNumber.from_integer(
                self.total_nodes(environment)
            )

        # log10(
        #   (b^(d+1)-1)/(b-1)
        # )
        #
        # This avoids constructing the huge integer.
        power = depth + 1

        leading = (
            power
            * math.log10(branching)
        )

        correction = math.log10(
            1.0
            - branching ** (-power)
        )

        denominator = math.log10(
            branching - 1
        )

        return SEAHugeNumber(
            log10_value=(
                leading
                + correction
                - denominator
            )
        )

    def growth_form(self):
        branching = _expr(self.branching)
        depth = _expr(self.depth)

        return {
            "frontier": (
                f"({branching}) ^ ({depth})"
            ),
            "total_nodes": (
                f"sum_{{i=0..{depth}}} "
                f"({branching})^i"
            ),
        }


@dataclass(frozen=True)
class SEASearchProfile:
    name: str
    search_space: SEASearchSpace
    node_cost: float = 1.0

    def estimated_work(self, environment=None):
        return (
            self.search_space.total_nodes(
                environment
            )
            * self.node_cost
        )

    def summary(self, environment=None):
        return {
            "name": self.name,
            "growth": self.search_space.growth_form(),
            "total_nodes": (
                self.search_space.total_nodes(
                    environment
                )
            ),
            "estimated_work": (
                self.estimated_work(environment)
            ),
        }
