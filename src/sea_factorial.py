from dataclasses import dataclass
import math

from src.sea_huge import SEAHugeNumber


@dataclass(frozen=True)
class SEAFactorial:
    n: int

    def __post_init__(self):
        if self.n < 0:
            raise ValueError(
                "factorial domain requires n >= 0"
            )

    def exact(self):
        return math.factorial(self.n)

    def log10(self):
        if self.n <= 1:
            return 0.0

        return math.lgamma(
            self.n + 1
        ) / math.log(10)

    def huge(self):
        return SEAHugeNumber(
            self.log10()
        )

    def digits(self):
        if self.n <= 1:
            return 1

        return int(
            math.floor(
                self.log10()
            )
        ) + 1

    def stirling_log10(self):
        if self.n == 0:
            return 0.0

        n = float(self.n)

        return (
            n * math.log10(n / math.e)
            + 0.5 * math.log10(
                2 * math.pi * n
            )
        )
