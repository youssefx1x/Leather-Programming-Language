from dataclasses import dataclass
from src.sea_state import SEAState, SEATransition


@dataclass(frozen=True)
class SEAHistory:
    initial: SEAState
    transitions: tuple = ()

    @property
    def current(self):
        if not self.transitions:
            return self.initial

        return self.transitions[-1].target

    @property
    def depth(self):
        return len(self.transitions)

    def append(self, transition):
        if transition.source != self.current:
            raise ValueError(
                "transition source does not match current state"
            )

        return SEAHistory(
            initial=self.initial,
            transitions=self.transitions + (transition,),
        )

    def states(self):
        return (
            (self.initial,)
            + tuple(
                transition.target
                for transition in self.transitions
            )
        )
