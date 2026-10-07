from dataclasses import dataclass, field


@dataclass(frozen=True)
class PlanStep:
    operation: str
    data: dict = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    steps: list[PlanStep] = field(default_factory=list)

    def add(self, operation, **data):
        self.steps.append(
            PlanStep(
                operation=operation,
                data=data,
            )
        )

    def describe(self):
        lines = ["PLAN"]

        for step in self.steps:
            operation = step.operation
            data = step.data

            if operation == "DEFINE":
                lines.append(
                    f"  DEFINE {data['name']} = "
                    f"{data['value']}"
                )

            elif operation == "CHECK":
                lines.append(
                    f"    CHECK "
                    f"{data['object']}."
                    f"{data['member']}"
                )

            elif operation == "IF_TRUE":
                lines.append("    IF TRUE")

            elif operation == "EFFECT":
                lines.append(
                    f"      {data['target']} "
                    f"{data['operator']} "
                    f"{data['value']}"
                )

            elif operation == "RULE":
                lines.append(
                    f"  RULE {data['name']}"
                )

        return "\n".join(lines)


class SemanticPlanner:
    def plan(self, semantic_program):
        plan = ExecutionPlan()

        for definition in semantic_program.definitions:
            plan.add(
                "DEFINE",
                name=definition.name,
                value=definition.value.value,
            )

        for rule in semantic_program.rules:
            plan.add(
                "RULE",
                name=rule.name,
            )

            plan.add(
                "CHECK",
                object=rule.condition.object_name,
                member=rule.condition.member_name,
            )

            plan.add("IF_TRUE")

            plan.add(
                "EFFECT",
                target=rule.effect.target,
                operator=rule.effect.operator,
                value=rule.effect.value.value,
            )

        return plan
