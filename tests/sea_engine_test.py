from src.sea import SEAClass, SEAValue
from src.sea_engine import SEAEngine


def main():
    engine = SEAEngine()

    # Regular computation
    result = engine.evaluate(
        "add",
        2,
        3,
    )

    assert result.kind == SEAClass.REGULAR
    assert result.value == 5

    # 0 / 0 becomes an explicit SEA state
    result = engine.evaluate(
        "divide",
        0,
        0,
    )

    assert result.kind == SEAClass.EXCEPTIONAL
    assert result.context.operation == "divide"
    assert result.context.reason == "zero_divided_by_zero"

    # Exceptional states propagate through the registry.
    result = engine.evaluate(
        "add",
        result,
        5,
    )

    assert result.kind == SEAClass.EXCEPTIONAL
    assert result.context.operation == "add"
    assert result.context.reason == "exceptional_operand"

    # Engine accepts SEAValue directly.
    result = engine.evaluate(
        "multiply",
        SEAValue.regular(4),
        SEAValue.regular(5),
    )

    assert result.kind == SEAClass.REGULAR
    assert result.value == 20

    print("SEA 0.1 ENGINE: PASS")


if __name__ == "__main__":
    main()
