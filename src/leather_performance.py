from dataclasses import dataclass

from src.integration.sea_bridge import (
    LEATHERSEABridge,
)
from src.optimizer.performance_model import (
    PerformanceEstimate,
)
from src.optimizer.performance_optimizer import (
    PerformanceOptimizer,
)
from src.optimizer.performance_plan import (
    OptimizationCandidate,
)
from src.runtime.performance_evidence import (
    PerformanceEvidence,
)
from src.runtime.performance_runtime import (
    PerformanceRuntime,
)
from src.semantic.performance_intent import (
    PerformanceIntent,
)


@dataclass(frozen=True)
class LeatherOptimizationResult:
    source: PerformanceEstimate
    plan: object
    sea_certificate: object
    evidence: object

    @property
    def valid(self):
        return (
            self.plan.valid
            and self.sea_certificate.valid
            and self.evidence.valid
        )


class LeatherPerformanceEngine:
    def __init__(self):
        self.optimizer = PerformanceOptimizer()
        self.runtime = PerformanceRuntime()

    def optimize(
        self,
        source,
        candidates=(),
        function=None,
        optimized_function=None,
        intent=None,
    ):
        intent = (
            intent
            if intent is not None
            else PerformanceIntent()
        )

        plan = self.optimizer.optimize(
            source,
            candidates,
        )

        if plan.selected is None:
            raise ValueError(
                "no verified improving candidate"
            )

        sea_certificate = (
            LEATHERSEABridge.certificate(
                name=plan.selected.name,
                source_cost=source.cost,
                target_cost=plan.selected.cost,
                semantics_preserved=(
                    intent.preserve_semantics
                    and plan.selected.semantics_preserved
                ),
            )
        )

        source_output = None
        target_output = None
        elapsed_ns = 0

        if (
            function is not None
            and optimized_function is not None
        ):
            baseline = self.runtime.measure(
                function
            )

            optimized = self.runtime.measure(
                optimized_function
            )

            source_output = baseline.result
            target_output = optimized.result
            elapsed_ns = optimized.elapsed_ns
        else:
            source_output = source.name
            target_output = plan.selected.name

        evidence = PerformanceEvidence(
            name=plan.selected.name,
            source_output=source_output,
            target_output=target_output,
            source_cost=source.cost,
            target_cost=plan.selected.cost,
            semantics_preserved=(
                intent.preserve_semantics
                and plan.selected.semantics_preserved
            ),
            measured_elapsed_ns=elapsed_ns,
        )

        return LeatherOptimizationResult(
            source=source,
            plan=plan,
            sea_certificate=sea_certificate,
            evidence=evidence,
        )
