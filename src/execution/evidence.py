from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionEvidence:
    strategy: str
    source_result: object
    optimized_result: object
    source_operations: int
    optimized_operations: int
    source_elapsed_ns: int
    optimized_elapsed_ns: int
    semantics_preserved: bool

    @property
    def output_equal(self):
        return self.source_result == self.optimized_result

    @property
    def operations_reduced(self):
        return (
            self.optimized_operations
            < self.source_operations
        )

    @property
    def wall_clock_reduced(self):
        return (
            self.optimized_elapsed_ns
            < self.source_elapsed_ns
        )

    @property
    def valid(self):
        return (
            self.output_equal
            and self.semantics_preserved
            and self.operations_reduced
        )

    def summary(self):
        return {
            "strategy": self.strategy,
            "output_equal": self.output_equal,
            "operations_reduced":
                self.operations_reduced,
            "wall_clock_reduced":
                self.wall_clock_reduced,
            "semantics_preserved":
                self.semantics_preserved,
            "valid": self.valid,
        }
