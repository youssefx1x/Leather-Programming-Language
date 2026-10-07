from src.sea import SEAValue
from src.sea_rules import SEARuleRegistry, register_default_rules


class SEAEngine:
    """
    Initial SEA computational engine.

    The engine separates:
    - values
    - operations
    - rules
    - execution
    """

    def __init__(self, registry=None):
        self.registry = (
            registry
            if registry is not None
            else register_default_rules(
                SEARuleRegistry()
            )
        )

    def normalize(self, value):
        if isinstance(value, SEAValue):
            return value

        return SEAValue.regular(value)

    def evaluate(self, operation, left, right):
        left = self.normalize(left)
        right = self.normalize(right)

        result = self.registry.resolve(
            operation,
            left,
            right,
        )

        if result is not None:
            return result

        return self._evaluate_regular(
            operation,
            left,
            right,
        )

    def _evaluate_regular(self, operation, left, right):
        if not left.is_regular or not right.is_regular:
            raise ValueError(
                f"no SEA rule for {operation}"
            )

        if operation == "add":
            return SEAValue.regular(
                left.value + right.value
            )

        if operation == "subtract":
            return SEAValue.regular(
                left.value - right.value
            )

        if operation == "multiply":
            return SEAValue.regular(
                left.value * right.value
            )

        if operation == "divide":
            if right.value == 0:
                if left.value == 0:
                    return SEAValue.exceptional(
                        "divide",
                        (left, right),
                        "zero_divided_by_zero",
                    )

                return SEAValue.exceptional(
                    "divide",
                    (left, right),
                    "division_by_zero",
                )

            return SEAValue.regular(
                left.value / right.value
            )

        raise ValueError(
            f"unknown SEA operation '{operation}'"
        )
