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


class BaseFlowMeaning:
    def __init__(self):
        self.root = MeaningNode("PROGRAM")

    def add_base(self, base):
        node = MeaningNode(
            "BASE",
            name=base.name,
            data={
                "service": base.service,
            },
        )

        for option in base.options:
            node.add(
                MeaningNode(
                    "OPTION",
                    name=option.name,
                    data={
                        "value": option.value,
                    },
                )
            )

        self.root.add(node)

    def add_extension(self, extension):
        node = MeaningNode(
            "BASE_EXTENSION",
            name=extension.name,
            data={
                "base": extension.base_name,
            },
        )

        for option in extension.options:
            node.add(
                MeaningNode(
                    "OPTION",
                    name=option.name,
                    data={
                        "value": option.value,
                    },
                )
            )

        self.root.add(node)

    def add_flow(self, flow):
        node = MeaningNode(
            "FLOW",
            name=flow.name,
        )

        for index, step in enumerate(flow.steps):
            node.add(
                MeaningNode(
                    "STEP",
                    name=step,
                    data={
                        "index": index,
                    },
                )
            )

        self.root.add(node)

    def describe(self):
        lines = ["MEANING"]

        def visit(node, depth=0):
            indent = "  " * depth

            label = node.kind

            if node.name is not None:
                label += f" {node.name}"

            if "service" in node.data:
                label += f" [service={node.data['service']}]"

            if "base" in node.data:
                label += f" [base={node.data['base']}]"

            if "value" in node.data:
                label += f" [{node.data['value']}]"

            lines.append(indent + label)

            for child in node.children:
                visit(child, depth + 1)

        visit(self.root)

        return "\n".join(lines)
