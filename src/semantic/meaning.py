from dataclasses import dataclass, field


@dataclass
class MeaningNode:
    kind: str
    name: str | None = None
    data: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def add(self, child):
        self.children.append(child)
        return child


class MeaningGraph:
    def __init__(self):
        self.root = MeaningNode("PROGRAM")

    def add_definition(self, name, value):
        node = MeaningNode(
            "DEFINE",
            name=name,
            data={"value": value},
        )
        self.root.add(node)
        return node

    def add_rule(self, rule):
        node = MeaningNode(
            "RULE",
            name=rule.name,
        )

        condition = MeaningNode(
            "CONDITION",
            data={
                "object": rule.condition.object_name,
                "member": rule.condition.member_name,
            },
        )

        effect = MeaningNode(
            "EFFECT",
            data={
                "target": rule.action_target,
                "operator": rule.action_operator,
                "value": rule.action_value,
            },
        )

        node.add(condition)
        node.add(effect)
        self.root.add(node)

        return node

    def describe(self):
        lines = []

        def format_data(node):
            if node.kind == "CONDITION":
                return (
                    f"{node.data['object']}."
                    f"{node.data['member']}"
                )

            if node.kind == "EFFECT":
                value = node.data["value"]

                if hasattr(value, "value"):
                    value = value.value

                return (
                    f"{node.data['target']} "
                    f"{node.data['operator']} "
                    f"{value}"
                )

            if node.kind == "DEFINE":
                value = node.data["value"]

                if hasattr(value, "value"):
                    value = value.value

                return f"{node.name} = {value}"

            return None

        def visit(node, depth=0):
            indent = "  " * depth

            label = node.kind

            if node.name is not None:
                label += f" {node.name}"

            details = format_data(node)

            if details is not None:
                label += f" [{details}]"

            lines.append(indent + label)

            for child in node.children:
                visit(child, depth + 1)

        visit(self.root)

        return "\n".join(lines)
