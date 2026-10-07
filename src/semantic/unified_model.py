from dataclasses import dataclass, field


@dataclass
class UnifiedSemanticProgram:
    definitions: list = field(default_factory=list)
    rules: list = field(default_factory=list)
    bases: list = field(default_factory=list)
    extensions: list = field(default_factory=list)
    flows: list = field(default_factory=list)
    systems: list = field(default_factory=list)

    # Core 0.2 computational semantics
    domains: list = field(default_factory=list)
    states: list = field(default_factory=list)
    operations: list = field(default_factory=list)
    transitions: list = field(default_factory=list)

    def all_items(self):
        return (
            list(self.definitions)
            + list(self.rules)
            + list(self.bases)
            + list(self.extensions)
            + list(self.flows)
            + list(self.systems)
            + list(self.domains)
            + list(self.states)
            + list(self.operations)
            + list(self.transitions)
        )

    def counts(self):
        return {
            "definitions": len(self.definitions),
            "rules": len(self.rules),
            "bases": len(self.bases),
            "extensions": len(self.extensions),
            "flows": len(self.flows),
            "systems": len(self.systems),
            "domains": len(self.domains),
            "states": len(self.states),
            "operations": len(self.operations),
            "transitions": len(self.transitions),
        }
