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


class SystemMeaning:
    def __init__(self):
        self.root = MeaningNode("PROGRAM")

    def add_system(self, system):
        node = MeaningNode(
            "SYSTEM",
            name=system.name,
        )

        for index, component in enumerate(system.components):
            node.add(
                MeaningNode(
                    "COMPONENT",
                    name=component,
                    data={"index": index},
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

            if "index" in node.data:
                label += f" [index={node.data['index']}]"

            lines.append(indent + label)

            for child in node.children:
                visit(child, depth + 1)

        visit(self.root)

        return "\n".join(lines)
