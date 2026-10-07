from dataclasses import dataclass, field


@dataclass(frozen=True)
class SemanticValue:
    kind: str
    value: object


@dataclass(frozen=True)
class SemanticDefinition:
    name: str
    value: SemanticValue


@dataclass(frozen=True)
class SemanticCondition:
    object_name: str
    member_name: str


@dataclass(frozen=True)
class SemanticEffect:
    target: str
    operator: str
    value: SemanticValue


@dataclass(frozen=True)
class SemanticRule:
    name: str
    condition: SemanticCondition
    effect: SemanticEffect


@dataclass
class SemanticProgram:
    definitions: list[SemanticDefinition] = field(default_factory=list)
    rules: list[SemanticRule] = field(default_factory=list)
