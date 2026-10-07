from src.sea import SEAClass
from src.sea_engine import SEAEngine


def assert_regular(result, expected):
    assert result.kind == SEAClass.REGULAR
    assert result.value == expected


def main():
    engine = SEAEngine()

    # ---------------------------------
    # 1. Closure
    # ---------------------------------
    operations = (
        ("add", 2, 3),
        ("subtract", 7, 2),
        ("multiply", 4, 5),
        ("divide", 10, 2),
    )

    for operation, left, right in operations:
        result = engine.evaluate(
            operation,
            left,
            right,
        )

        assert isinstance(result.value, (int, float))
        assert result.kind == SEAClass.REGULAR

    # ---------------------------------
    # 2. Associativity
    # (a + b) + c = a + (b + c)
    # ---------------------------------
    left = engine.evaluate(
        "add",
        engine.evaluate("add", 2, 3),
        4,
    )

    right = engine.evaluate(
        "add",
        2,
        engine.evaluate("add", 3, 4),
    )

    assert_regular(left, 9)
    assert_regular(right, 9)
    assert left.value == right.value

    # ---------------------------------
    # 3. Multiplicative associativity
    # (a * b) * c = a * (b * c)
    # ---------------------------------
    left = engine.evaluate(
        "multiply",
        engine.evaluate("multiply", 2, 3),
        4,
    )

    right = engine.evaluate(
        "multiply",
        2,
        engine.evaluate("multiply", 3, 4),
    )

    assert_regular(left, 24)
    assert_regular(right, 24)
    assert left.value == right.value

    # ---------------------------------
    # 4. Distributivity
    # a * (b + c) = (a*b) + (a*c)
    # ---------------------------------
    left = engine.evaluate(
        "multiply",
        2,
        engine.evaluate("add", 3, 4),
    )

    right = engine.evaluate(
        "add",
        engine.evaluate("multiply", 2, 3),
        engine.evaluate("multiply", 2, 4),
    )

    assert_regular(left, 14)
    assert_regular(right, 14)
    assert left.value == right.value

    # ---------------------------------
    # 5. Exceptional closure
    # 0 / 0 must remain inside SEA.
    # ---------------------------------
    exceptional = engine.evaluate(
        "divide",
        0,
        0,
    )

    assert exceptional.kind == SEAClass.EXCEPTIONAL
    assert exceptional.context.operation == "divide"
    assert exceptional.context.reason == "zero_divided_by_zero"

    # ---------------------------------
    # 6. Exceptional propagation
    # ---------------------------------
    propagated = engine.evaluate(
        "multiply",
        exceptional,
        10,
    )

    assert propagated.kind == SEAClass.EXCEPTIONAL
    assert propagated.context.operation == "multiply"

    print("SEA 0.1 ALGEBRA CONSISTENCY: PASS")


if __name__ == "__main__":
    main()
