from src.optimizer.adaptive_model import (
    OptimizedExecutionPlan,
    OptimizationReport,
)


class AdaptiveOptimizer:
    """
    Optimize a UnifiedExecutionPlan using semantic decisions
    and resource constraints.

    The optimizer changes execution strategy, not program meaning.
    """

    def optimize(self, plan, intent=None, envelope=None):
        intent = intent
        envelope = envelope

        report = OptimizationReport()

        # Work on the existing plan object structure without
        # changing the semantic program.
        optimized_plan = plan

        self._optimize_flows(
            optimized_plan,
            intent,
            envelope,
            report,
        )

        self._optimize_definitions(
            optimized_plan,
            intent,
            envelope,
            report,
        )

        self._optimize_systems(
            optimized_plan,
            intent,
            envelope,
            report,
        )

        return OptimizedExecutionPlan(
            original_plan=plan,
            plan=optimized_plan,
            report=report,
        )

    def _decision(self, intent, name):
        if intent is None:
            return None

        return intent.get_decision(name)

    def _optimize_flows(
        self,
        plan,
        intent,
        envelope,
        report,
    ):
        execution = self._decision(
            intent,
            "execution.mode",
        )

        compute = self._decision(
            intent,
            "compute.target",
        )

        for step in plan.steps:
            if step.kind != "FLOW":
                continue

            if execution:
                mode = execution["value"]

                if mode == "latency":
                    step.details["optimization"] = "latency"
                    step.details["scheduling"] = "eager"

                    report.add(
                        step.name,
                        "latency",
                        execution["reason"],
                        scheduling="eager",
                    )

                elif mode == "streaming":
                    step.details["optimization"] = "streaming"
                    step.details["scheduling"] = "stream"

                    report.add(
                        step.name,
                        "streaming",
                        execution["reason"],
                        scheduling="stream",
                    )

                elif mode == "balanced":
                    step.details["optimization"] = "balanced"

                    report.add(
                        step.name,
                        "balanced",
                        execution["reason"],
                    )

            if compute:
                target = compute["value"]

                if target == "gpu":
                    step.details["compute_target"] = "gpu"

                    report.add(
                        step.name,
                        "gpu",
                        compute["reason"],
                        compute_target="gpu",
                    )

    def _optimize_definitions(
        self,
        plan,
        intent,
        envelope,
        report,
    ):
        memory = self._decision(
            intent,
            "memory.strategy",
        )

        for step in plan.steps:
            if step.kind != "DEFINE":
                continue

            if memory:
                strategy = memory["value"]

                step.details[
                    "memory_optimization"
                ] = strategy

                report.add(
                    step.name,
                    f"memory-{strategy}",
                    memory["reason"],
                    memory_strategy=strategy,
                )

    def _optimize_systems(
        self,
        plan,
        intent,
        envelope,
        report,
    ):
        if envelope is None:
            return

        cpu = envelope.cpu

        if cpu is None or cpu < 2:
            return

        for step in plan.steps:
            if step.kind != "SYSTEM":
                continue

            components = step.details.get(
                "components",
                (),
            )

            if len(components) >= 2:
                step.details["scheduling"] = "parallel-capable"

                report.add(
                    step.name,
                    "parallel-capable",
                    "multiple system components and sufficient CPU resources",
                    cpu=cpu,
                )
