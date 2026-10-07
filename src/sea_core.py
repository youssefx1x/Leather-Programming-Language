from dataclasses import dataclass, field

from src.sea import SEAValue
from src.sea_complexity import SEAComplexity


@dataclass(frozen=True)
class SEAMathematicalState:
    """
    Mathematical state of the SEA system.

    A state combines:
    - semantic value
    - context
    - complexity structure
    """

    value: SEAValue
    complexity: SEAComplexity = field(
        default_factory=SEAComplexity.constant
    )
    context: tuple = ()
    label: str = "state"


@dataclass(frozen=True)
class SEAMathematicalTransition:
    source: SEAMathematicalState
    operation: str
    target: SEAMathematicalState
    rule: str
    semantics_preserved: bool = True


@dataclass(frozen=True)
class SEAStateSequence:
    initial: SEAMathematicalState
    transitions: tuple = ()

    @property
    def current(self):
        if not self.transitions:
            return self.initial

        return self.transitions[-1].target

    def append(self, transition):
        if transition.source != self.current:
            raise ValueError(
                "transition source does not match "
                "current SEA mathematical state"
            )

        return SEAStateSequence(
            initial=self.initial,
            transitions=self.transitions + (
                transition,
            ),
        )

    def depth(self):
        return len(self.transitions)
