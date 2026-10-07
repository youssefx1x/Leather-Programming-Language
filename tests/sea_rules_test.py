from src.sea import SEAClass, SEAValue
from src.sea_rules import (
    SEARule,
    SEARuleRegistry,
    register_default_rules,
)


def main():
    registry = SEARuleRegistry()

    register_default_rules(registry)

    assert len(registry.rules_for("add")) == 1
    assert len(registry.rules_for("subtract")) == 1
    assert len(registry.rules_for("multiply")) == 1
    assert len(registry.rules_for("divide")) == 1

    exceptional = SEAValue.exceptional(
        "divide",
        (0, 0),
        "zero_divided_by_zero",
    )

    result = registry.resolve(
        "add",
        exceptional,
        SEAValue.regular(5),
    )

    assert result is not None
    assert result.kind == SEAClass.EXCEPTIONAL

    assert result.context.operation == "add"
    assert result.context.reason == "exceptional_operand"

    # No registered rule for an unrelated operation.
    assert registry.resolve(
        "unknown_operation",
        SEAValue.regular(1),
        SEAValue.regular(2),
    ) is None

    print("SEA 0.1 RULE REGISTRY: PASS")


if __name__ == "__main__":
    main()
