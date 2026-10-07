from src.sea import SEAClass, SEAValue
from src.sea_engine import SEAEngine
from src.sea_state import (
    SEAState,
    SEATransition,
    SEATransitionEngine,
)


def main():
    engine = SEAEngine()
    transition_engine = SEATransitionEngine(engine)

    initial = SEAState(
        value=SEAValue.regular(10),
        label="initial",
    )

    transition = transition_engine.transition(
        initial,
        "add",
        5,
    )

    assert isinstance(transition, SEATransition)
    assert transition.source == initial
    assert transition.operation == "add"
    assert transition.operands == (5,)

    assert transition.target.value.kind == SEAClass.REGULAR
    assert transition.target.value.value == 15
    assert transition.target.label == "add_result"

    exceptional = transition_engine.transition(
        initial,
        "divide",
        -10,
    )

    assert exceptional.target.value.kind == SEAClass.REGULAR
    assert exceptional.target.value.value == -1

    zero_state = SEAState(
        value=SEAValue.regular(0),
        label="zero",
    )

    undefined = transition_engine.transition(
        zero_state,
        "divide",
        0,
    )

    assert undefined.target.value.kind == SEAClass.EXCEPTIONAL
    assert undefined.target.value.context.operation == "divide"
    assert (
        undefined.target.value.context.reason
        == "zero_divided_by_zero"
    )

    print("SEA 0.1 TRANSITION MODEL: PASS")


if __name__ == "__main__":
    main()
