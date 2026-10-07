from dataclasses import dataclass
from fractions import Fraction


def _to_expr(value):
    if isinstance(value, ComplexityExpr):
        return value

    return ComplexityExpr.const(value)


@dataclass(frozen=True)
class ComplexityExpr:
    """
    Symbolic complexity expression.

    Supported forms:
    - constant
    - symbol
    - add
    - mul
    - pow
    - max
    """

    op: str
    args: tuple = ()

    @classmethod
    def const(cls, value):
        if isinstance(value, Fraction):
            return cls("const", (value,))

        if isinstance(value, int):
            return cls("const", (Fraction(value),))

        if isinstance(value, float):
            return cls("const", (Fraction(value),))

        raise TypeError("complexity constant must be numeric")

    @classmethod
    def symbol(cls, name):
        if not isinstance(name, str) or not name:
            raise ValueError("symbol name must be non-empty")

        return cls("symbol", (name,))

    @classmethod
    def add(cls, left, right):
        left = _to_expr(left)
        right = _to_expr(right)

        if left.op == "const" and right.op == "const":
            return cls.const(
                left.args[0] + right.args[0]
            )

        if left.op == "const" and left.args[0] == 0:
            return right

        if right.op == "const" and right.args[0] == 0:
            return left

        return cls("add", (left, right))

    @classmethod
    def mul(cls, left, right):
        left = _to_expr(left)
        right = _to_expr(right)

        if (
            left.op == "const"
            and left.args[0] == 0
        ):
            return cls.const(0)

        if (
            right.op == "const"
            and right.args[0] == 0
        ):
            return cls.const(0)

        if (
            left.op == "const"
            and left.args[0] == 1
        ):
            return right

        if (
            right.op == "const"
            and right.args[0] == 1
        ):
            return left

        if left.op == "const" and right.op == "const":
            return cls.const(
                left.args[0] * right.args[0]
            )

        return cls("mul", (left, right))

    @classmethod
    def power(cls, base, exponent):
        base = _to_expr(base)
        exponent = _to_expr(exponent)

        if (
            exponent.op == "const"
            and exponent.args[0] == 0
        ):
            return cls.const(1)

        if (
            exponent.op == "const"
            and exponent.args[0] == 1
        ):
            return base

        if (
            base.op == "const"
            and exponent.op == "const"
        ):
            return cls.const(
                base.args[0] ** exponent.args[0]
            )

        return cls("pow", (base, exponent))

    @classmethod
    def maximum(cls, left, right):
        left = _to_expr(left)
        right = _to_expr(right)

        if left == right:
            return left

        if left.op == "const" and right.op == "const":
            return cls.const(
                max(left.args[0], right.args[0])
            )

        return cls("max", (left, right))

    def __add__(self, other):
        return self.add(self, other)

    def __radd__(self, other):
        return self.add(other, self)

    def __mul__(self, other):
        return self.mul(self, other)

    def __rmul__(self, other):
        return self.mul(other, self)

    def __pow__(self, other):
        return self.power(self, other)

    def __rpow__(self, other):
        return self.power(other, self)

    def evaluate(self, environment=None):
        environment = environment or {}

        if self.op == "const":
            return self.args[0]

        if self.op == "symbol":
            name = self.args[0]

            if name not in environment:
                raise KeyError(
                    f"missing complexity symbol '{name}'"
                )

            return environment[name]

        if self.op == "add":
            return (
                self.args[0].evaluate(environment)
                + self.args[1].evaluate(environment)
            )

        if self.op == "mul":
            return (
                self.args[0].evaluate(environment)
                * self.args[1].evaluate(environment)
            )

        if self.op == "pow":
            return (
                self.args[0].evaluate(environment)
                ** self.args[1].evaluate(environment)
            )

        if self.op == "max":
            return max(
                self.args[0].evaluate(environment),
                self.args[1].evaluate(environment),
            )

        raise ValueError(
            f"unknown complexity operation '{self.op}'"
        )

    def is_numeric(self):
        if self.op == "const":
            return True

        if self.op == "symbol":
            return False

        return all(
            arg.is_numeric()
            for arg in self.args
        )

    def numeric_value(self):
        if not self.is_numeric():
            raise ValueError(
                "complexity expression is symbolic"
            )

        return self.evaluate()

    def __str__(self):
        if self.op == "const":
            value = self.args[0]

            if value.denominator == 1:
                return str(value.numerator)

            return str(value)

        if self.op == "symbol":
            return self.args[0]

        if self.op == "add":
            return (
                f"({self.args[0]} + {self.args[1]})"
            )

        if self.op == "mul":
            return (
                f"({self.args[0]} * {self.args[1]})"
            )

        if self.op == "pow":
            return (
                f"({self.args[0]} ^ {self.args[1]})"
            )

        if self.op == "max":
            return (
                f"max({self.args[0]}, {self.args[1]})"
            )

        return f"{self.op}{self.args}"


@dataclass(frozen=True)
class SEAComplexity:
    time: ComplexityExpr
    memory: ComplexityExpr
    states: ComplexityExpr
    branching: ComplexityExpr
    depth: ComplexityExpr
    precision: ComplexityExpr
    interactions: ComplexityExpr

    def __post_init__(self):
        for name in (
            "time",
            "memory",
            "states",
            "branching",
            "depth",
            "precision",
            "interactions",
        ):
            value = getattr(self, name)

            if not isinstance(value, ComplexityExpr):
                object.__setattr__(
                    self,
                    name,
                    ComplexityExpr.const(value),
                )

    @classmethod
    def constant(cls, value=1):
        value = ComplexityExpr.const(value)

        return cls(
            time=value,
            memory=value,
            states=value,
            branching=value,
            depth=value,
            precision=value,
            interactions=value,
        )

    @classmethod
    def zero(cls):
        return cls.constant(0)

    def sequential(self, other):
        """
        Generic sequential composition model.

        Time/depth/interactions accumulate.
        Memory/state/branching/precision use maximum.
        """
        return SEAComplexity(
            time=self.time + other.time,
            memory=ComplexityExpr.maximum(
                self.memory,
                other.memory,
            ),
            states=ComplexityExpr.maximum(
                self.states,
                other.states,
            ),
            branching=ComplexityExpr.maximum(
                self.branching,
                other.branching,
            ),
            depth=self.depth + other.depth,
            precision=ComplexityExpr.maximum(
                self.precision,
                other.precision,
            ),
            interactions=(
                self.interactions
                + other.interactions
            ),
        )

    def dominates_numeric(self, other):
        """
        Return True if this vector is no worse than
        'other' in every component and strictly better
        in at least one numeric component.
        """
        mine = self.numeric_tuple()
        theirs = other.numeric_tuple()

        if mine is None or theirs is None:
            return False

        all_not_worse = all(
            left <= right
            for left, right in zip(mine, theirs)
        )

        strictly_better = any(
            left < right
            for left, right in zip(mine, theirs)
        )

        return all_not_worse and strictly_better

    def numeric_tuple(self):
        values = (
            self.time,
            self.memory,
            self.states,
            self.branching,
            self.depth,
            self.precision,
            self.interactions,
        )

        if not all(
            value.is_numeric()
            for value in values
        ):
            return None

        return tuple(
            value.numeric_value()
            for value in values
        )

    def render(self):
        return {
            "time": str(self.time),
            "memory": str(self.memory),
            "states": str(self.states),
            "branching": str(self.branching),
            "depth": str(self.depth),
            "precision": str(self.precision),
            "interactions": str(self.interactions),
        }
