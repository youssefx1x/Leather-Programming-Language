from src.sea import SEAClass, SEAValue
from src.sea_operations import (
    add,
    subtract,
    multiply,
    divide,
)


def main():
    # Regular arithmetic
    assert add(2, 3).value == 5
    assert subtract(7, 2).value == 5
    assert multiply(4, 3).value == 12
    assert divide(10, 2).value == 5

    # 0 / 0
    zero_zero = divide(0, 0)

    assert zero_zero.kind == SEAClass.EXCEPTIONAL
    assert zero_zero.context.operation == "divide"
    assert zero_zero.context.operands == (
        SEAValue.regular(0),
        SEAValue.regular(0),
    )
    assert zero_zero.context.reason == "zero_divided_by_zero"

    # infinity - infinity
    infinity_minus_infinity = subtract(
        SEAValue.infinite(),
        SEAValue.infinite(),
    )

    assert infinity_minus_infinity.kind == SEAClass.EXCEPTIONAL
    assert (
        infinity_minus_infinity.context.reason
        == "infinity_minus_infinity"
    )

    # zero * infinity
    zero_times_infinity = multiply(
        0,
        SEAValue.infinite(),
    )

    assert zero_times_infinity.kind == SEAClass.EXCEPTIONAL
    assert (
        zero_times_infinity.context.reason
        == "zero_times_infinity"
    )

    # regular / infinity
    finite_over_infinity = divide(
        10,
        SEAValue.infinite(),
    )

    assert finite_over_infinity.kind == SEAClass.REGULAR
    assert finite_over_infinity.value == 0

    print("SEA 0.1 OPERATIONS: PASS")


if __name__ == "__main__":
    main()
