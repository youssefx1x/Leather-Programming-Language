from dataclasses import dataclass

from src.execution.counter import ExecutionCounter
from src.execution.evidence import ExecutionEvidence
from src.execution.measurement import ExecutionMeasurer
from src.execution.selector import ExecutionStrategySelector


@dataclass(frozen=True)
class ExecutionResult:
    decision: object
    evidence: ExecutionEvidence

    @property
    def valid(self):
        return self.evidence.valid


class LeatherExecutionEngine:
    def __init__(self):
        self.selector = ExecutionStrategySelector()
        self.measurer = ExecutionMeasurer()

    def decide(self, workload):
        return self.selector.select(workload)

    def compare(
        self,
        workload,
        source_function,
        optimized_function,
        semantics_preserved=True,
    ):
        decision = self.decide(workload)

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

        evidence = ExecutionEvidence(
            strategy=decision.strategy.value,
            source_result=source.result,
            optimized_result=optimized.result,
            source_operations=source.operations,
            optimized_operations=optimized.operations,
            source_elapsed_ns=source.elapsed_ns,
            optimized_elapsed_ns=optimized.elapsed_ns,
            semantics_preserved=semantics_preserved,
        )

        return ExecutionResult(
            decision=decision,
            evidence=evidence,
        )
