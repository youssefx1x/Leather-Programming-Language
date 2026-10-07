from dataclasses import dataclass
from src.sea import SEAValue


@dataclass(frozen=True)
class SEAState:
    value: SEAValue
    label: str = "state"


@dataclass(frozen=True)
class SEATransition:
    source: SEAState
    operation: str
    operands: tuple
    target: SEAState
    reason: str = "operation"


class SEATransitionEngine:
    def __init__(self, engine):
        self.engine = engine

    def transition(self, state, operation, *operands):
        result = self.engine.evaluate(
            operation,
            state.value,
            *operands,
        )

        target = SEAState(
            value=result,
            label=f"{operation}_result",
        )

        return SEATransition(
            source=state,
            operation=operation,
            operands=tuple(operands),
            target=target,
            reason="operation",
        )
