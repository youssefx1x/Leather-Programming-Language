from dataclasses import dataclass, field


@dataclass
class LeatherProgram:
    source: str
    tokens: list = field(default_factory=list)
    ast: object = None
    semantic: object = None
    ir: object = None


@dataclass
class LeatherResult:
    success: bool
    value: object = None
    error: str | None = None
    elapsed_ns: int = 0
