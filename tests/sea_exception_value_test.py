from src.sea import SEAClass, SEAValue
from src.sea_exceptions import SEAExceptionalClass
from src.sea_engine import SEAEngine


def main():
    engine = SEAEngine()

    zero_over_zero = engine.evaluate(
        "divide",
        0,
        0,
    )

    assert zero_over_zero.kind == SEAClass.EXCEPTIONAL

    assert (
        zero_over_zero.exceptional_class
        == SEAExceptionalClass.ZERO_OVER_ZERO
    )

    assert (
        zero_over_zero.context.exceptional_class
        == SEAExceptionalClass.ZERO_OVER_ZERO
    )

    infinity_minus_infinity = SEAValue.exceptional(
        "subtract",
        (),
        "infinity_minus_infinity",
    )

    assert (
        infinity_minus_infinity.exceptional_class
        == SEAExceptionalClass.INFINITY_MINUS_INFINITY
    )

    division_by_zero = engine.evaluate(
        "divide",
        5,
        0,
    )

    assert (
        division_by_zero.exceptional_class
        == SEAExceptionalClass.DIVISION_BY_ZERO
    )

    regular = SEAValue.regular(10)

    assert regular.exceptional_class is None

    print("SEA 0.1 EXCEPTIONAL VALUE CLASSIFICATION: PASS")


if __name__ == "__main__":
    main()
