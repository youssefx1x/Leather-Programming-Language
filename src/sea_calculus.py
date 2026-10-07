from dataclasses import dataclass
import math

from src.sea_complexity import ComplexityExpr


def _expr(value):
    if isinstance(value, ComplexityExpr):
        return value

    return ComplexityExpr.const(value)


@dataclass(frozen=True)
class ComplexityFunction:
    name: str
    expression: ComplexityExpr
    variable: str = "n"

    def evaluate(self, n):
        return self.expression.evaluate(
            {self.variable: n}
        )

    def __str__(self):
        return f"{self.name}({self.variable}) = {self.expression}"


def constant(value):
    return ComplexityFunction(
        name="constant",
        expression=_expr(value),
    )


def logarithmic(variable="n"):
    n = ComplexityExpr.symbol(variable)

    return ComplexityFunction(
        name="log",
        expression=ComplexityExpr(
            "log",
            (n,),
        ),
        variable=variable,
    )


def exponential(base=2, variable="n"):
    n = ComplexityExpr.symbol(variable)

    return ComplexityFunction(
        name="exponential",
        expression=ComplexityExpr.power(
            base,
            n,
        ),
        variable=variable,
    )


def polynomial(power, variable="n"):
    n = ComplexityExpr.symbol(variable)

    return ComplexityFunction(
        name=f"polynomial_{power}",
        expression=n ** power,
        variable=variable,
    )


def linear(variable="n"):
    return polynomial(1, variable)


def quadratic(variable="n"):
    return polynomial(2, variable)


def cubic(variable="n"):
    return polynomial(3, variable)


def sqrt(variable="n"):
    n = ComplexityExpr.symbol(variable)

    return ComplexityFunction(
        name="sqrt",
        expression=ComplexityExpr(
            "sqrt",
            (n,),
        ),
        variable=variable,
    )


def evaluate_expression(expr, environment):
    if expr.op == "const":
        return float(expr.args[0])

    if expr.op == "symbol":
        return float(
            environment[expr.args[0]]
        )

    if expr.op == "add":
        return (
            evaluate_expression(
                expr.args[0],
                environment,
            )
            + evaluate_expression(
                expr.args[1],
                environment,
            )
        )

    if expr.op == "mul":
        return (
            evaluate_expression(
                expr.args[0],
                environment,
            )
            * evaluate_expression(
                expr.args[1],
                environment,
            )
        )

    if expr.op == "pow":
        base = evaluate_expression(
            expr.args[0],
            environment,
        )
        exponent = evaluate_expression(
            expr.args[1],
            environment,
        )

        return base ** exponent

    if expr.op == "max":
        return max(
            evaluate_expression(
                expr.args[0],
                environment,
            ),
            evaluate_expression(
                expr.args[1],
                environment,
            ),
        )

    if expr.op == "log":
        value = evaluate_expression(
            expr.args[0],
            environment,
        )

        return math.log(value)

    if expr.op == "sqrt":
        value = evaluate_expression(
            expr.args[0],
            environment,
        )

        return math.sqrt(value)

    raise ValueError(
        f"unsupported complexity expression '{expr.op}'"
    )


def _patch_evaluation():
    original = ComplexityExpr.evaluate

    def evaluate(self, environment=None):
        environment = environment or {}

        if self.op in {
            "log",
            "sqrt",
        }:
            return evaluate_expression(
                self,
                environment,
            )

        return original(
            self,
            environment,
        )

    ComplexityExpr.evaluate = evaluate


_patch_evaluation()


def compare_growth(
    first,
    second,
    points=(10, 100, 1000),
):
    first_values = []
    second_values = []

    for n in points:
        first_values.append(
            first.evaluate(n)
        )
        second_values.append(
            second.evaluate(n)
        )

    first_total = sum(first_values)
    second_total = sum(second_values)

    if math.isclose(
        first_total,
        second_total,
        rel_tol=1e-9,
        abs_tol=1e-12,
    ):
        relation = "equivalent"

    elif first_total < second_total:
        relation = "slower_growth"

    else:
        relation = "faster_growth"

    return {
        "relation": relation,
        "first": tuple(first_values),
        "second": tuple(second_values),
    }


@dataclass(frozen=True)
class GrowthClass:
    name: str
    rank: int


GROWTH_CLASSES = (
    GrowthClass("constant", 0),
    GrowthClass("logarithmic", 1),
    GrowthClass("sqrt", 2),
    GrowthClass("linear", 3),
    GrowthClass("quadratic", 4),
    GrowthClass("cubic", 5),
    GrowthClass("polynomial", 6),
    GrowthClass("exponential", 7),
)


def growth_rank(name):
    for item in GROWTH_CLASSES:
        if item.name == name:
            return item.rank

    raise ValueError(
        f"unknown growth class '{name}'"
    )
