from dataclasses import dataclass
import math

from src.sea_huge import SEAHugeNumber


@dataclass(frozen=True)
class SEAStateSpaceAlgebra:
    dimensions: tuple

    def product(self, other):
        return SEAStateSpaceAlgebra(
            self.dimensions
            + other.dimensions
        )

    def total_states(self):
        result = 1

        for dimension in self.dimensions:
            if dimension < 0:
                raise ValueError(
                    "dimension cannot be negative"
                )

            result *= dimension

        return result

    def log10_states(self):
        if any(
            dimension == 0
            for dimension in self.dimensions
        ):
            return float("-inf")

        return sum(
            math.log10(dimension)
            for dimension in self.dimensions
            if dimension > 0
        )

    def huge_states(self):
        return SEAHugeNumber(
            self.log10_states()
        )

    def add_alternatives(self, other):
        return SEAAlternativeSpace(
            spaces=(self, other)
        )


@dataclass(frozen=True)
class SEAAlternativeSpace:
    spaces: tuple

    def total_states(self):
        return sum(
            space.total_states()
            for space in self.spaces
        )

    def log10_states(self):
        total = self.total_states()

        if total == 0:
            return float("-inf")

        return math.log10(total)

    def huge_states(self):
        return SEAHugeNumber(
            self.log10_states()
        )


@dataclass(frozen=True)
class SEACompressedStateClasses:
    raw_states: int
    equivalence_classes: int

    def __post_init__(self):
        if self.raw_states < 0:
            raise ValueError(
                "raw state count cannot be negative"
            )

        if self.equivalence_classes < 0:
            raise ValueError(
                "class count cannot be negative"
            )

        if (
            self.raw_states > 0
            and self.equivalence_classes == 0
        ):
            raise ValueError(
                "nonzero raw space cannot map to zero classes"
            )

    @property
    def ratio(self):
        if self.equivalence_classes == 0:
            return 1.0

        return (
            self.raw_states
            / self.equivalence_classes
        )

    @property
    def reduction(self):
        if self.raw_states == 0:
            return 0.0

        return (
            1
            - self.equivalence_classes
            / self.raw_states
        )

    @property
    def valid_compression(self):
        return (
            self.equivalence_classes
            < self.raw_states
        )
