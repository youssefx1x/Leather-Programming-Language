from src.ir.ir import LTHIR
from src.ir.unified_compiler import UnifiedIRCompiler
from src.optimizer.evidence import OptimizationEvidenceLog


class OptimizedIRCompiler:
    """
    Compile a unified semantic program and attach
    optimization metadata/evidence from the execution plan.
    """

    def __init__(self):
        self.base_compiler = UnifiedIRCompiler()

    def compile(
        self,
        semantic_program,
        optimized_plan=None,
    ):
        ir = self.base_compiler.compile(
            semantic_program
        )

        evidence = OptimizationEvidenceLog()

        if optimized_plan is not None:
            self._apply_plan_metadata(
                ir,
                optimized_plan,
                evidence,
            )

        return ir, evidence

    def _apply_plan_metadata(
        self,
        ir,
        optimized_plan,
        evidence,
    ):
        for step in optimized_plan.plan.steps:
            optimization = step.details.get(
                "optimization"
            )

            if optimization is not None:
                reason = self._find_reason(
                    optimized_plan,
                    step.name,
                    optimization,
                )

                evidence.record(
                    step.name,
                    optimization,
                    reason,
                    "adaptive_optimizer",
                )

                ir.emit(
                    "OPTIMIZATION_HINT",
                    step.kind,
                    step.name,
                    optimization,
                )

            memory = step.details.get(
                "memory_optimization"
            )

            if memory is not None:
                reason = self._find_reason(
                    optimized_plan,
                    step.name,
                    f"memory-{memory}",
                )

                evidence.record(
                    step.name,
                    f"memory-{memory}",
                    reason,
                    "adaptive_optimizer",
                )

                ir.emit(
                    "OPTIMIZATION_HINT",
                    step.kind,
                    step.name,
                    f"memory:{memory}",
                )

            compute = step.details.get(
                "compute_target"
            )

            if compute is not None:
                reason = self._find_reason(
                    optimized_plan,
                    step.name,
                    "gpu",
                )

                evidence.record(
                    step.name,
                    "gpu",
                    reason,
                    "adaptive_optimizer",
                )

                ir.emit(
                    "OPTIMIZATION_HINT",
                    step.kind,
                    step.name,
                    f"compute:{compute}",
                )

            scheduling = step.details.get(
                "scheduling"
            )

            if scheduling is not None:
                reason = self._find_reason(
                    optimized_plan,
                    step.name,
                    scheduling,
                )

                evidence.record(
                    step.name,
                    f"scheduling:{scheduling}",
                    reason,
                    "adaptive_optimizer",
                )

                ir.emit(
                    "OPTIMIZATION_HINT",
                    step.kind,
                    step.name,
                    f"scheduling:{scheduling}",
                )

    def _find_reason(
        self,
        optimized_plan,
        step_name,
        strategy,
    ):
        for decision in optimized_plan.report.decisions:
            if (
                decision.step_name == step_name
                and decision.strategy == strategy
            ):
                return decision.reason

        return "optimization strategy selected by planner"
