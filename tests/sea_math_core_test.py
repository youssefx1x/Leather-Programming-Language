from src.sea import SEAClass, SEAValue
from src.sea_complexity import (
    ComplexityExpr,
    SEAComplexity,
)
from src.sea_core import (
    SEAMathematicalState,
    SEAMathematicalTransition,
    SEAStateSequence,
)


def main():
    n = ComplexityExpr.symbol("n")

    polynomial = n ** 2
    exponential = 2 ** n
    combined = polynomial * exponential

    assert str(polynomial) == "(n ^ 2)"
    assert str(exponential) == "(2 ^ n)"
    assert combined.evaluate({"n": 10}) == 102400

    complexity = SEAComplexity(
        time=combined,
        memory=n,
        states=exponential,
        branching=2,
        depth=n,
        precision=1,
        interactions=n * 3,
    )

    rendered = complexity.render()

    assert rendered["time"] == "((n ^ 2) * (2 ^ n))"
    assert rendered["states"] == "(2 ^ n)"

    state = SEAMathematicalState(
        value=SEAValue.regular(42),
        complexity=complexity,
        context=("core",),
        label="initial",
    )

    transition_target = SEAMathematicalState(
        value=SEAValue.regular(84),
        complexity=SEAComplexity.constant(2),
        context=("core",),
        label="next",
    )

    transition = SEAMathematicalTransition(
        source=state,
        operation="multiply",
        target=transition_target,
        rule="regular_multiplication",
    )

    sequence = SEAStateSequence(
        initial=state
    ).append(transition)

    assert sequence.current.value.kind == SEAClass.REGULAR
    assert sequence.current.value.value == 84
    assert sequence.current.label == "next"
    assert sequence.depth() == 1

    print("SEA 0.1 MATHEMATICAL CORE: PASS")


if __name__ == "__main__":
    main()
