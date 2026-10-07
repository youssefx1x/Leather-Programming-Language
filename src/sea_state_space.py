from dataclasses import dataclass
import math

from src.sea_huge import SEAHugeNumber


@dataclass(frozen=True)
class SEAStateSpace:
    dimensions: tuple

    @property
    def dimension_count(self):
        return len(self.dimensions)

    def state_count(self):
        total = 1

        for dimension in self.dimensions:
            if dimension < 0:
                raise ValueError(
                    "state dimension cannot be negative"
                )

            total *= dimension

        return total

    def huge_state_count(self):
        total_log10 = 0.0

        for dimension in self.dimensions:
            if dimension <= 0:
                return SEAHugeNumber(
                    float("-inf")
                )

            total_log10 += math.log10(
                dimension
            )

        return SEAHugeNumber(
            total_log10
        )

    def entropy_like_measure(self):
        """
        Structural measure:

            H = log2(N)

        where N is the total state count.
        """
        count = self.huge_state_count()

        if math.isinf(count.log10_value):
            return float("-inf")

        return (
            count.log10_value
            * math.log2(10)
        )


@dataclass(frozen=True)
class SEACompressedSpace:
    original: SEAStateSpace
    compression_factor: int

    def compressed_state_count(self):
        original = self.original.huge_state_count()

        if self.compression_factor <= 0:
            raise ValueError(
                "compression factor must be positive"
            )

        return SEAHugeNumber(
            original.log10_value
            - math.log10(
                self.compression_factor
            )
        )

    def reduction_ratio(self):
        return self.compression_factor
