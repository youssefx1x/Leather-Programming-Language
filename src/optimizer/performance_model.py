from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceCost:
    time: float = 0.0
    memory: float = 0.0
    states: float = 0.0
    branching: float = 0.0
    depth: float = 0.0
    precision: float = 0.0
    interactions: float = 0.0

    def __post_init__(self):
        values = (
            self.time,
            self.memory,
            self.states,
            self.branching,
            self.depth,
            self.precision,
            self.interactions,
        )

        if any(value < 0 for value in values):
            raise ValueError("performance cost values must be >= 0")

    def numeric_tuple(self):
        return (
            self.time,
            self.memory,
            self.states,
            self.branching,
            self.depth,
            self.precision,
            self.interactions,
        )

    def total(self):
        return sum(self.numeric_tuple())

    def add(self, other):
        return PerformanceCost(
            time=self.time + other.time,
            memory=self.memory + other.memory,
            states=self.states + other.states,
            branching=self.branching + other.branching,
            depth=self.depth + other.depth,
            precision=self.precision + other.precision,
            interactions=self.interactions + other.interactions,
        )

    def scale(self, factor):
        if factor < 0:
            raise ValueError("scale factor must be >= 0")

        return PerformanceCost(
            time=self.time * factor,
            memory=self.memory * factor,
            states=self.states * factor,
            branching=self.branching * factor,
            depth=self.depth * factor,
            precision=self.precision * factor,
            interactions=self.interactions * factor,
        )

    def dominates(self, other):
        mine = self.numeric_tuple()
        theirs = other.numeric_tuple()

        no_worse = all(
            left <= right
            for left, right in zip(mine, theirs)
        )

        strictly_better = any(
            left < right
            for left, right in zip(mine, theirs)
        )

        return no_worse and strictly_better

    def equal(self, other):
        return self.numeric_tuple() == other.numeric_tuple()

    def render(self):
        return {
            "time": self.time,
            "memory": self.memory,
            "states": self.states,
            "branching": self.branching,
            "depth": self.depth,
            "precision": self.precision,
            "interactions": self.interactions,
            "total": self.total(),
        }


@dataclass(frozen=True)
class PerformanceEstimate:
    name: str
    cost: PerformanceCost
    meaning_signature: str
    assumptions: tuple = ()

    def describe(self):
        return {
            "name": self.name,
            "cost": self.cost.render(),
            "meaning_signature": self.meaning_signature,
            "assumptions": self.assumptions,
        }
