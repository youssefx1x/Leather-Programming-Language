from dataclasses import dataclass

from src.execution.engine import LeatherExecutionEngine
from src.execution.model import ExecutionWorkload
from src.semantic.execution_intent import ExecutionIntent


@dataclass(frozen=True)
class LeatherExecutionReport:
    workload: ExecutionWorkload
    intent: ExecutionIntent
    decision: object
    evidence: object

    @property
    def valid(self):
        return self.evidence.valid


class LeatherExecution:
    def __init__(self):
        self.engine = LeatherExecutionEngine()

    def run(
        self,
        workload,
        source_function,
        optimized_function,
        intent=None,
    ):
        intent = (
            intent
            if intent is not None
            else ExecutionIntent()
        )

        decision = self.engine.decide(workload)

        if not intent.permits(
            decision.strategy.value
        ):
            raise ValueError(
                "selected execution strategy is not permitted"
            )

        result = self.engine.compare(
            workload=workload,
            source_function=source_function,
            optimized_function=optimized_function,
            semantics_preserved=intent.preserve_semantics,
        )

        return LeatherExecutionReport(
            workload=workload,
            intent=intent,
            decision=result.decision,
            evidence=result.evidence,
        )
