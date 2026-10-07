from src.sea import (
    SEAClass,
    SEAValue,
)


def main():
    regular = SEAValue.regular(5)

    assert regular.kind == SEAClass.REGULAR
    assert regular.value == 5
    assert regular.is_regular

    infinite = SEAValue.infinite()

    assert infinite.kind == SEAClass.INFINITE
    assert infinite.is_infinite

    exceptional = SEAValue.exceptional(
        operation="divide",
        operands=(0, 0),
        reason="zero_divided_by_zero",
    )

    assert exceptional.kind == SEAClass.EXCEPTIONAL
    assert exceptional.is_exceptional

    assert exceptional.context.operation == "divide"
    assert exceptional.context.operands == (0, 0)
    assert exceptional.context.reason == "zero_divided_by_zero"

    print("SEA 0.1 VALUE MODEL: PASS")


if __name__ == "__main__":
    main()
