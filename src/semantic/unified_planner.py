from dataclasses import dataclass, field


@dataclass(frozen=True)
class UnifiedPlanStep:
    kind: str
    name: str
    details: dict = field(default_factory=dict)


@dataclass
class UnifiedExecutionPlan:
    steps: list = field(default_factory=list)

    def add(self, kind, name, **details):
        step = UnifiedPlanStep(
            kind=kind,
            name=name,
            details=details,
        )
        self.steps.append(step)
        return step

    def describe(self):
        lines = ["UNIFIED EXECUTION PLAN"]

        for index, step in enumerate(self.steps):
            lines.append(
                f"  {index:04d} {step.kind} {step.name}"
            )

            for key, value in step.details.items():
                lines.append(
                    f"         {key} = {value}"
                )

        return "\n".join(lines)
