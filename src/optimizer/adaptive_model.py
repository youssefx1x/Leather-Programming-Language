from dataclasses import dataclass, field


@dataclass(frozen=True)
class OptimizationDecision:
    step_name: str
    strategy: str
    reason: str
    changes: dict = field(default_factory=dict)


@dataclass
class OptimizationReport:
    decisions: list = field(default_factory=list)

    def add(self, step_name, strategy, reason, **changes):
        decision = OptimizationDecision(
            step_name=step_name,
            strategy=strategy,
            reason=reason,
            changes=changes,
        )

        self.decisions.append(decision)
        return decision

    def describe(self):
        lines = ["OPTIMIZATION REPORT"]

        if not self.decisions:
            lines.append("  no optimizations applied")
            return "\n".join(lines)

        for decision in self.decisions:
            lines.append(
                f"  {decision.step_name}: "
                f"{decision.strategy}"
            )

            lines.append(
                f"    reason = {decision.reason}"
            )

            for key, value in decision.changes.items():
                lines.append(
                    f"    {key} = {value}"
                )

        return "\n".join(lines)


@dataclass
class OptimizedExecutionPlan:
    original_plan: object
    plan: object
    report: OptimizationReport = field(
        default_factory=OptimizationReport
    )

    def describe(self):
        lines = [
            self.plan.describe(),
            "",
            self.report.describe(),
        ]

        return "\n".join(lines)
