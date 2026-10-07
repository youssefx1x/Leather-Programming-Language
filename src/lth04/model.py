from dataclasses import dataclass, field


class LTH04Error(Exception):
    pass


@dataclass(frozen=True)
class Instruction:
    op: str
    arg: object = None


@dataclass(frozen=True)
class BytecodeProgram:
    instructions: tuple
    source_hash: str
    prepared_source: str
    statement_count: int
    flow_names: tuple = ()
    system_names: tuple = ()
    base_names: tuple = ()
    optimized: bool = False


@dataclass
class ExecutionStats:
    cache_hit: bool = False
    instruction_count: int = 0
    elapsed: float = 0.0
    trace: list = field(default_factory=list)
