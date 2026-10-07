from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SEAHugeNumber:
    """
    Log-domain representation of a positive huge number.

    Represents approximately:

        value = mantissa * base ** exponent

    without requiring construction of the complete integer.
    """

    log10_value: float

    @classmethod
    def from_integer(cls, value):
        if value <= 0:
            raise ValueError(
                "huge number must be positive"
            )

        return cls(
            log10_value=math.log10(value)
        )

    @classmethod
    def power(cls, base, exponent):
        if base <= 0:
            raise ValueError(
                "base must be positive"
            )

        return cls(
            log10_value=(
                math.log10(base)
                * exponent
            )
        )

    @property
    def decimal_digits(self):
        if self.log10_value < 0:
            return 1

        return int(
            math.floor(self.log10_value)
        ) + 1

    @property
    def scientific_exponent(self):
        return math.floor(
            self.log10_value
        )

    @property
    def scientific_mantissa(self):
        exponent = self.scientific_exponent

        return 10 ** (
            self.log10_value - exponent
        )

    def log10(self):
        return self.log10_value

    def compare(self, other):
        if self.log10_value < other.log10_value:
            return -1

        if self.log10_value > other.log10_value:
            return 1

        return 0

    def render(self):
        return (
            f"{self.scientific_mantissa:.6g}"
            f"e{self.scientific_exponent}"
        )
