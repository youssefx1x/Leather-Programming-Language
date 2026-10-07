from src.sea import SEAClass, SEAValue
from src.sea_engine import SEAEngine
from src.sea_state import SEAState, SEATransitionEngine
from src.sea_history import SEAHistory


def main():
    engine = SEAEngine()
    transition_engine = SEATransitionEngine(engine)

    initial = SEAState(
        value=SEAValue.regular(10),
        label="initial",
    )

    history = SEAHistory(initial=initial)

    first = transition_engine.transition(
        history.current,
        "add",
        5,
    )

    history = history.append(first)

    assert history.depth == 1
    assert history.current.value.value == 15

    second = transition_engine.transition(
        history.current,
        "multiply",
        2,
    )

    history = history.append(second)

    assert history.depth == 2
    assert history.current.value.kind == SEAClass.REGULAR
    assert history.current.value.value == 30

    states = history.states()

    assert len(states) == 3
    assert states[0].value.value == 10
    assert states[1].value.value == 15
    assert states[2].value.value == 30

    invalid_state = SEAState(
        value=SEAValue.regular(999),
        label="invalid",
    )

    invalid_transition = transition_engine.transition(
        invalid_state,
        "add",
        1,
    )

    try:
        history.append(invalid_transition)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "invalid transition was accepted"
        )

    zero = SEAState(
        value=SEAValue.regular(0),
        label="zero",
    )

    exceptional = transition_engine.transition(
        zero,
        "divide",
        0,
    )

    history = SEAHistory(
        initial=zero
    ).append(exceptional)

    assert history.current.value.kind == SEAClass.EXCEPTIONAL
    assert (
        history.current.value.context.reason
        == "zero_divided_by_zero"
    )

    print("SEA 0.1 HISTORY & PROVENANCE: PASS")


if __name__ == "__main__":
    main()
