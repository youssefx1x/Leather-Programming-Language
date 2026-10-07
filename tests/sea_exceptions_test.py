from src.sea_exceptions import (
    SEAExceptionalClass,
    SEAExceptionalReason,
)


def main():
    assert (
        SEAExceptionalReason.from_reason(
            "zero_divided_by_zero"
        )
        == SEAExceptionalClass.ZERO_OVER_ZERO
    )

    assert (
        SEAExceptionalReason.from_reason(
            "infinity_minus_infinity"
        )
        == SEAExceptionalClass.INFINITY_MINUS_INFINITY
    )

    assert (
        SEAExceptionalReason.from_reason(
            "infinity_divided_by_infinity"
        )
        == SEAExceptionalClass.INFINITY_OVER_INFINITY
    )

    assert (
        SEAExceptionalReason.from_reason(
            "zero_times_infinity"
        )
        == SEAExceptionalClass.ZERO_TIMES_INFINITY
    )

    assert (
        SEAExceptionalReason.from_reason(
            "division_by_zero"
        )
        == SEAExceptionalClass.DIVISION_BY_ZERO
    )

    assert (
        SEAExceptionalReason.from_reason(
            "exceptional_operand"
        )
        == SEAExceptionalClass.EXCEPTIONAL_OPERAND
    )

    assert (
        SEAExceptionalReason.from_reason(
            "something_unknown"
        )
        == SEAExceptionalClass.UNDEFINED_OPERATION
    )

    assert len(SEAExceptionalClass) == 7

    print("SEA 0.1 EXCEPTIONAL TAXONOMY: PASS")


if __name__ == "__main__":
    main()
