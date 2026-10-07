class UnifiedMeaningGraph:
    def __init__(self):
        self.nodes = []

    def add(self, kind, name, details=None):
        node = {
            "kind": kind,
            "name": name,
            "details": details or {},
        }
        self.nodes.append(node)
        return node

    def describe(self):
        lines = ["UNIFIED MEANING GRAPH"]

        for node in self.nodes:
            kind = node["kind"]
            name = node["name"]

            lines.append(f"  {kind} {name}")

            details = node["details"]

            for key, value in details.items():
                lines.append(
                    f"    {key} = {value}"
                )

        return "\n".join(lines)


class UnifiedMeaningBuilder:
    def build(self, semantic_program):
        graph = UnifiedMeaningGraph()

        for definition in semantic_program.definitions:
            name = getattr(definition, "name", str(definition))
            graph.add("DEFINE", name)

        for rule in semantic_program.rules:
            name = getattr(rule, "name", str(rule))
            graph.add("RULE", name)

        for base in semantic_program.bases:
            name = getattr(base, "name", str(base))
            graph.add("BASE", name)

        for extension in semantic_program.extensions:
            name = getattr(extension, "name", str(extension))
            base_name = getattr(extension, "base_name", None)
            graph.add(
                "BASE_EXTENSION",
                name,
                {"base": base_name},
            )

        for flow in semantic_program.flows:
            name = getattr(flow, "name", str(flow))
            graph.add("FLOW", name)

        for system in semantic_program.systems:
            name = getattr(system, "name", str(system))
            graph.add("SYSTEM", name)

        return graph
