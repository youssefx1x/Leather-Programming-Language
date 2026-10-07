from dataclasses import dataclass

from src.sea_complexity import ComplexityExpr, SEAComplexity


def _expr(value):
    if isinstance(value, ComplexityExpr):
        return value
    return ComplexityExpr.const(value)


def _sum(left, right):
    return _expr(left) + _expr(right)


def _max(left, right):
    return ComplexityExpr.maximum(
        _expr(left),
        _expr(right),
    )


def sequential_law(first, second):
    """
    Sequential composition:
    stage 2 starts after stage 1.
    """
    return SEAComplexity(
        time=_sum(first.time, second.time),
        memory=_max(first.memory, second.memory),
        states=_max(first.states, second.states),
        branching=_max(first.branching, second.branching),
        depth=_sum(first.depth, second.depth),
        precision=_max(first.precision, second.precision),
        interactions=_sum(first.interactions, second.interactions),
    )


def parallel_law(first, second):
    """
    Parallel composition under independent-resource assumptions.
    """
    return SEAComplexity(
        time=_max(first.time, second.time),
        memory=_sum(first.memory, second.memory),
        states=_sum(first.states, second.states),
        branching=_max(first.branching, second.branching),
        depth=_max(first.depth, second.depth),
        precision=_max(first.precision, second.precision),
        interactions=_sum(first.interactions, second.interactions),
    )


@dataclass(frozen=True)
class SEASearchLaw:
    branching: int
    depth: int

    def frontier_nodes(self):
        if self.branching < 0 or self.depth < 0:
            raise ValueError(
                "branching and depth must be non-negative"
            )

        return self.branching ** self.depth

    def total_nodes(self):
        if self.branching < 0 or self.depth < 0:
            raise ValueError(
                "branching and depth must be non-negative"
            )

        if self.branching == 0:
            return 1

        if self.branching == 1:
            return self.depth + 1

        return (
            self.branching ** (self.depth + 1) - 1
        ) // (self.branching - 1)

    def growth_expression(self):
        b = ComplexityExpr.const(self.branching)
        d = ComplexityExpr.symbol("d")
        return b ** d


@dataclass(frozen=True)
class SEAComplexityLawSet:
    name: str = "SEA 0.2 Core Laws"

    def sequential(self, first, second):
        return sequential_law(first, second)

    def parallel(self, first, second):
        return parallel_law(first, second)

    def search(self, branching, depth):
        return SEASearchLaw(
            branching=branching,
            depth=depth,
        )
