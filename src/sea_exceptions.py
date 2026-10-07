from enum import Enum


class SEAExceptionalClass(Enum):
    ZERO_OVER_ZERO = "zero_over_zero"
    INFINITY_MINUS_INFINITY = "infinity_minus_infinity"
    INFINITY_OVER_INFINITY = "infinity_over_infinity"
    ZERO_TIMES_INFINITY = "zero_times_infinity"
    DIVISION_BY_ZERO = "division_by_zero"
    EXCEPTIONAL_OPERAND = "exceptional_operand"
    UNDEFINED_OPERATION = "undefined_operation"


class SEAExceptionalReason:
    @staticmethod
    def from_reason(reason):
        mapping = {
            "zero_divided_by_zero":
                SEAExceptionalClass.ZERO_OVER_ZERO,

            "infinity_minus_infinity":
                SEAExceptionalClass.INFINITY_MINUS_INFINITY,

            "infinity_divided_by_infinity":
                SEAExceptionalClass.INFINITY_OVER_INFINITY,

            "zero_times_infinity":
                SEAExceptionalClass.ZERO_TIMES_INFINITY,

            "division_by_zero":
                SEAExceptionalClass.DIVISION_BY_ZERO,

            "exceptional_operand":
                SEAExceptionalClass.EXCEPTIONAL_OPERAND,
        }

        return mapping.get(
            reason,
            SEAExceptionalClass.UNDEFINED_OPERATION,
        )
