from dataclasses import dataclass

from src.execution.counter import ExecutionCounter
from src.execution.measurement import ExecutionMeasurer


@dataclass(frozen=True)
class BenchmarkResult:
    source_result: object
    optimized_result: object
    source_operations: int
    optimized_operations: int
    source_elapsed_ns: int
    optimized_elapsed_ns: int
    semantics_preserved: bool

    @property
    def output_equal(self):
        return (
            self.source_result
            == self.optimized_result
        )

    @property
    def operations_saved(self):
        return (
            self.source_operations
            - self.optimized_operations
        )

    @property
    def operation_reduction_ratio(self):
        if self.source_operations == 0:
            return 0.0

        return self.operations_saved / (
            self.source_operations
        )

    @property
    def valid(self):
        return (
            self.output_equal
            and self.semantics_preserved
            and self.operations_saved > 0
        )

    def summary(self):
        return {
            "output_equal": self.output_equal,
            "source_operations":
                self.source_operations,
            "optimized_operations":
                self.optimized_operations,
            "operations_saved":
                self.operations_saved,
            "operation_reduction_ratio":
                self.operation_reduction_ratio,
            "source_elapsed_ns":
                self.source_elapsed_ns,
            "optimized_elapsed_ns":
                self.optimized_elapsed_ns,
            "semantics_preserved":
                self.semantics_preserved,
            "valid": self.valid,
        }


class ExecutionBenchmark:
    def __init__(self):
        self.measurer = ExecutionMeasurer()

    def compare(
        self,
        source_function,
        optimized_function,
        semantics_preserved=True,
    ):
        source_counter = ExecutionCounter()
        optimized_counter = ExecutionCounter()

        source = self.measurer.measure(
            source_function,
            source_counter,
        )

        optimized = self.measurer.measure(
            optimized_function,
            optimized_counter,
        )

        return BenchmarkResult(
            source_result=source.result,
            optimized_result=optimized.result,
            source_operations=source.operations,
            optimized_operations=optimized.operations,
            source_elapsed_ns=source.elapsed_ns,
            optimized_elapsed_ns=optimized.elapsed_ns,
            semantics_preserved=semantics_preserved,
        )
