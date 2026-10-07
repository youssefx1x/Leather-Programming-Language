from dataclasses import dataclass
from enum import Enum

from src.sea_complexity import ComplexityExpr


class SEAAsymptoticKind(Enum):
    O = "O"
    OMEGA = "Omega"
    THETA = "Theta"
    EXACT = "Exact"


def _expr(value):
    if isinstance(value, ComplexityExpr):
        return value
    return ComplexityExpr.const(value)


@dataclass(frozen=True)
class SEAGrowthClass:
    name: str
    rank: int


GROWTH_ORDER = (
    SEAGrowthClass("constant", 0),
    SEAGrowthClass("logarithmic", 1),
    SEAGrowthClass("sqrt", 2),
    SEAGrowthClass("linear", 3),
    SEAGrowthClass("quadratic", 4),
    SEAGrowthClass("cubic", 5),
    SEAGrowthClass("polynomial", 6),
    SEAGrowthClass("exponential", 7),
)


def _constant_value(expr):
    if expr.op != "const":
        return None
    return expr.args[0]


def classify_growth(expression):
    expression = _expr(expression)

    if expression.op == "const":
        return "constant"

    if expression.op == "log":
        return "logarithmic"

    if expression.op == "sqrt":
        return "sqrt"

    if expression.op == "symbol":
        return "linear"

    if expression.op == "pow":
        base, exponent = expression.args
        base_const = _constant_value(base)
        exponent_const = _constant_value(exponent)

        if exponent_const is not None:
            if exponent_const == 1:
                return "linear"
            if exponent_const == 2:
                return "quadratic"
            if exponent_const == 3:
                return "cubic"
            if exponent_const > 3:
                return "polynomial"

        if base_const is not None and exponent.op == "symbol":
            if base_const > 1:
                return "exponential"

    if expression.op == "mul":
        left, right = expression.args
        left_class = classify_growth(left)
        right_class = classify_growth(right)

        polynomial_classes = {
            "constant",
            "linear",
            "quadratic",
            "cubic",
            "polynomial",
        }

        if left_class in polynomial_classes and right_class in polynomial_classes:
            return "polynomial"

        if "exponential" in {left_class, right_class}:
            return "exponential"

    return "unknown"


def growth_rank(name):
    for item in GROWTH_ORDER:
        if item.name == name:
            return item.rank
    return -1


@dataclass(frozen=True)
class SEAGrowthRelation:
    left: ComplexityExpr
    right: ComplexityExpr
    relation: str
    left_class: str
    right_class: str


def symbolic_growth_relation(left, right):
    left = _expr(left)
    right = _expr(right)

    left_class = classify_growth(left)
    right_class = classify_growth(right)

    left_rank = growth_rank(left_class)
    right_rank = growth_rank(right_class)

    if left == right:
        relation = "equivalent"
    elif left_rank < right_rank:
        relation = "slower_growth"
    elif left_rank > right_rank:
        relation = "faster_growth"
    elif left_class != "unknown" and left_class == right_class:
        relation = "same_class"
    else:
        relation = "undetermined"

    return SEAGrowthRelation(
        left=left,
        right=right,
        relation=relation,
        left_class=left_class,
        right_class=right_class,
    )


@dataclass(frozen=True)
class SEAAsymptoticClaim:
    kind: SEAAsymptoticKind
    function: ComplexityExpr
    reference: ComplexityExpr
    statement: str

    def render(self):
        if self.kind == SEAAsymptoticKind.O:
            prefix = "O"
        elif self.kind == SEAAsymptoticKind.OMEGA:
            prefix = "Omega"
        elif self.kind == SEAAsymptoticKind.THETA:
            prefix = "Theta"
        else:
            prefix = "Exact"

        return f"{prefix}({self.reference})"
