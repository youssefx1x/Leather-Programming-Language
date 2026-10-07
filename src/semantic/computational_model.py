from dataclasses import dataclass, field


@dataclass(frozen=True)
class StateField:
    name: str
    semantic_type: str = "unknown"


@dataclass(frozen=True)
class State:
    name: str
    domain: str = "standard"
    fields: tuple[StateField, ...] = ()


@dataclass(frozen=True)
class OperationInput:
    name: str
    semantic_type: str = "unknown"


@dataclass(frozen=True)
class Operation:
    name: str
    inputs: tuple[OperationInput, ...] = ()


@dataclass(frozen=True)
class Transition:
    source_state: str
    operation: str
    target_state: str


@dataclass(frozen=True)
class Domain:
    name: str
    states: tuple[State, ...] = ()
    operations: tuple[Operation, ...] = ()
    transitions: tuple[Transition, ...] = ()
