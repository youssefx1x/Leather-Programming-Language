from dataclasses import dataclass


@dataclass(frozen=True)
class SEAMetrics:
    generated: int = 0
    expanded: int = 0
    unique_states: int = 0
    memory_states: int = 0
    elapsed_ns: int = 0
    depth: int = 0

    @property
    def seconds(self):
        return self.elapsed_ns / 1_000_000_000

    @property
    def duplicate_count(self):
        return max(
            0,
            self.generated - self.unique_states,
        )

    @property
    def compression_ratio(self):
        if self.unique_states == 0:
            return 1.0

        return self.generated / self.unique_states

    def as_dict(self):
        return {
            "generated": self.generated,
            "expanded": self.expanded,
            "unique_states": self.unique_states,
            "memory_states": self.memory_states,
            "elapsed_ns": self.elapsed_ns,
            "seconds": self.seconds,
            "depth": self.depth,
            "duplicate_count": self.duplicate_count,
            "compression_ratio": self.compression_ratio,
        }


@dataclass(frozen=True)
class SEAComparisonMetrics:
    baseline: SEAMetrics
    optimized: SEAMetrics

    @property
    def elapsed_reduction(self):
        if self.baseline.elapsed_ns == 0:
            return 0.0

        return 1.0 - (
            self.optimized.elapsed_ns
            / self.baseline.elapsed_ns
        )

    @property
    def generated_reduction(self):
        if self.baseline.generated == 0:
            return 0.0

        return 1.0 - (
            self.optimized.generated
            / self.baseline.generated
        )

    @property
    def state_reduction(self):
        if self.baseline.unique_states == 0:
            return 0.0

        return 1.0 - (
            self.optimized.unique_states
            / self.baseline.unique_states
        )

    def as_dict(self):
        return {
            "elapsed_reduction": self.elapsed_reduction,
            "generated_reduction": self.generated_reduction,
            "state_reduction": self.state_reduction,
        }
