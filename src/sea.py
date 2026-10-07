from dataclasses import dataclass
from enum import Enum

from src.sea_exceptions import SEAExceptionalReason


class SEAClass(Enum):
    REGULAR = "regular"
    INFINITE = "infinite"
    EXCEPTIONAL = "exceptional"


@dataclass(frozen=True)
class ExceptionalContext:
    operation: str
    operands: tuple
    reason: str
    exceptional_class: object = None


@dataclass(frozen=True)
class SEAValue:
    kind: SEAClass
    value: object = None
    context: ExceptionalContext = None

    @classmethod
    def regular(cls, value):
        return cls(
            kind=SEAClass.REGULAR,
            value=value,
        )

    @classmethod
    def infinite(cls, value=None):
        return cls(
            kind=SEAClass.INFINITE,
            value=value,
        )

    @classmethod
    def exceptional(
        cls,
        operation,
        operands,
        reason,
    ):
        return cls(
            kind=SEAClass.EXCEPTIONAL,
            context=ExceptionalContext(
                operation=operation,
                operands=tuple(operands),
                reason=reason,
                exceptional_class=(
                    SEAExceptionalReason.from_reason(
                        reason
                    )
                ),
            ),
        )

    @property
    def is_regular(self):
        return self.kind == SEAClass.REGULAR

    @property
    def is_infinite(self):
        return self.kind == SEAClass.INFINITE

    @property
    def is_exceptional(self):
        return self.kind == SEAClass.EXCEPTIONAL

    @property
    def exceptional_class(self):
        if not self.is_exceptional:
            return None

        return self.context.exceptional_class
