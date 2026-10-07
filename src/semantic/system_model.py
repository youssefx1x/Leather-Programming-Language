from dataclasses import dataclass, field


@dataclass(frozen=True)
class SemanticSystem:
    name: str
    components: tuple


@dataclass
class SemanticSystemProgram:
    systems: list[SemanticSystem] = field(default_factory=list)
