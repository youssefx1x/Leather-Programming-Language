from src.sea import SEAValue


class SEAOperationError(Exception):
    pass


def _unwrap(value):
    if isinstance(value, SEAValue):
        return value

    return SEAValue.regular(value)


def add(left, right):
    left = _unwrap(left)
    right = _unwrap(right)

    if left.is_exceptional or right.is_exceptional:
        return SEAValue.exceptional(
            "add",
            (left, right),
            "exceptional_operand",
        )

    if left.is_infinite or right.is_infinite:
        return SEAValue.exceptional(
            "add",
            (left, right),
            "infinite_combination_requires_rule",
        )

    return SEAValue.regular(
        left.value + right.value
    )


def subtract(left, right):
    left = _unwrap(left)
    right = _unwrap(right)

    if left.is_exceptional or right.is_exceptional:
        return SEAValue.exceptional(
            "subtract",
            (left, right),
            "exceptional_operand",
        )

    if left.is_infinite and right.is_infinite:
        return SEAValue.exceptional(
            "subtract",
            (left, right),
            "infinity_minus_infinity",
        )

    if left.is_infinite or right.is_infinite:
        return SEAValue.infinite()

    return SEAValue.regular(
        left.value - right.value
    )


def multiply(left, right):
    left = _unwrap(left)
    right = _unwrap(right)

    if left.is_exceptional or right.is_exceptional:
        return SEAValue.exceptional(
            "multiply",
            (left, right),
            "exceptional_operand",
        )

    if (
        (left.is_infinite and right.is_regular and right.value == 0)
        or
        (right.is_infinite and left.is_regular and left.value == 0)
    ):
        return SEAValue.exceptional(
            "multiply",
            (left, right),
            "zero_times_infinity",
        )

    if left.is_infinite or right.is_infinite:
        return SEAValue.infinite()

    return SEAValue.regular(
        left.value * right.value
    )


def divide(left, right):
    left = _unwrap(left)
    right = _unwrap(right)

    if left.is_exceptional or right.is_exceptional:
        return SEAValue.exceptional(
            "divide",
            (left, right),
            "exceptional_operand",
        )

    if right.is_regular and right.value == 0:
        if left.is_regular and left.value == 0:
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

    if left.is_infinite and right.is_infinite:
        return SEAValue.exceptional(
            "divide",
            (left, right),
            "infinity_divided_by_infinity",
        )

    if left.is_infinite:
        return SEAValue.infinite()

    if right.is_infinite:
        return SEAValue.regular(0)

    return SEAValue.regular(
        left.value / right.value
    )
