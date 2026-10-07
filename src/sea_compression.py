from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SEACompression:
    original_states: float
    compressed_states: float
    semantics_preserved: bool
    method: str
    evidence: str = ""

    def __post_init__(self):
        if self.original_states < 0:
            raise ValueError(
                "original state count cannot be negative"
            )

        if self.compressed_states < 0:
            raise ValueError(
                "compressed state count cannot be negative"
            )

        if (
            self.compressed_states == 0
            and self.original_states != 0
        ):
            raise ValueError(
                "compressed state count cannot be zero "
                "for a nonzero source"
            )

    @property
    def ratio(self):
        if self.original_states == 0:
            return 1.0

        return (
            self.original_states
            / self.compressed_states
        )

    @property
    def reduced(self):
        return (
            self.compressed_states
            < self.original_states
        )

    @property
    def valid(self):
        return (
            self.semantics_preserved
            and self.reduced
        )

    @property
    def percentage_reduction(self):
        if self.original_states == 0:
            return 0.0

        return 100.0 * (
            1.0
            - self.compressed_states
            / self.original_states
        )

    def summary(self):
        return {
            "method": self.method,
            "original_states": self.original_states,
            "compressed_states": self.compressed_states,
            "compression_ratio": self.ratio,
            "percentage_reduction": self.percentage_reduction,
            "semantics_preserved": self.semantics_preserved,
            "valid": self.valid,
        }


@dataclass(frozen=True)
class SEACompressionCertificate:
    transformation: SEACompression
    checks: tuple

    @property
    def valid(self):
        return (
            all(self.checks)
            and self.transformation.valid
        )

    def summary(self):
        return {
            "valid": self.valid,
            "checks": self.checks,
            "ratio": self.transformation.ratio,
        }


def certify_compression(transformation):
    checks = (
        transformation.original_states
        >= transformation.compressed_states,
        transformation.semantics_preserved,
        math.isfinite(transformation.ratio),
    )

    return SEACompressionCertificate(
        transformation=transformation,
        checks=checks,
    )
