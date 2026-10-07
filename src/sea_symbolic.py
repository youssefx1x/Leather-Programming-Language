from dataclasses import dataclass

from src.sea_complexity import ComplexityExpr


def _expr(value):
    if isinstance(value, ComplexityExpr):
        return value
    return ComplexityExpr.const(value)


def _const(expr):
    if expr.op == "const":
        return expr.args[0]
    return None


def _symbol(expr):
    if expr.op == "symbol":
        return expr.args[0]
    return None


def simplify(expr):
    expr = _expr(expr)

    if expr.op in {"const", "symbol"}:
        return expr

    args = tuple(
        simplify(arg)
        if isinstance(arg, ComplexityExpr)
        else arg
        for arg in expr.args
    )

    expr = ComplexityExpr(
        expr.op,
        args,
    )

    if expr.op == "add":
        left, right = expr.args
        lc = _const(left)
        rc = _const(right)

        if lc == 0:
            return right

        if rc == 0:
            return left

        if lc is not None and rc is not None:
            return ComplexityExpr.const(lc + rc)

        if left == right:
            return ComplexityExpr.mul(
                2,
                left,
            )

    if expr.op == "mul":
        left, right = expr.args
        lc = _const(left)
        rc = _const(right)

        if lc == 0 or rc == 0:
            return ComplexityExpr.const(0)

        if lc == 1:
            return right

        if rc == 1:
            return left

        if lc is not None and rc is not None:
            return ComplexityExpr.const(lc * rc)

        if left == right:
            return ComplexityExpr.power(
                left,
                2,
            )

    if expr.op == "pow":
        base, exponent = expr.args
        ec = _const(exponent)

        if ec == 0:
            return ComplexityExpr.const(1)

        if ec == 1:
            return base

        bc = _const(base)

        if bc == 0 and ec is not None and ec > 0:
            return ComplexityExpr.const(0)

        if bc == 1:
            return ComplexityExpr.const(1)

    if expr.op == "max":
        left, right = expr.args

        if left == right:
            return left

        lc = _const(left)
        rc = _const(right)

        if lc is not None and rc is not None:
            return ComplexityExpr.const(
                max(lc, rc)
            )

    return expr


@dataclass(frozen=True)
class SEASymbolicResult:
    original: ComplexityExpr
    simplified: ComplexityExpr

    @property
    def changed(self):
        return self.original != self.simplified

    def evaluate(self, environment=None):
        return self.simplified.evaluate(
            environment or {}
        )


def normalize(expr):
    previous = _expr(expr)

    for _ in range(16):
        current = simplify(previous)

        if current == previous:
            break

        previous = current

    return SEASymbolicResult(
        original=_expr(expr),
        simplified=previous,
    )
