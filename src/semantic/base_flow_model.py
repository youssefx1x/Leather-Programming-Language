from dataclasses import dataclass, field


@dataclass(frozen=True)
class SemanticOption:
    name: str
    value: object


@dataclass(frozen=True)
class SemanticBase:
    name: str
    service: str
    options: tuple = ()


@dataclass(frozen=True)
class SemanticBaseExtension:
    name: str
    base_name: str
    options: tuple = ()


@dataclass(frozen=True)
class SemanticFlow:
    name: str
    steps: tuple


@dataclass
class SemanticBaseFlowProgram:
    bases: list[SemanticBase] = field(default_factory=list)
    extensions: list[SemanticBaseExtension] = field(default_factory=list)
    flows: list[SemanticFlow] = field(default_factory=list)
