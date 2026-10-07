from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class SEARecurrence:
    """
    Linear recurrence:
        T(n) = sum(coeff[i] * T(n-i-1)) + forcing(n)
    """

    name: str
    initial: tuple
    coefficients: tuple
    forcing: object = 0

    def __post_init__(self):
        if not self.initial:
            raise ValueError("recurrence requires at least one initial value")

        if len(self.coefficients) != len(self.initial):
            raise ValueError(
                "coefficients and initial values must have equal length"
            )

    @property
    def order(self):
        return len(self.initial)

    def _forcing(self, n):
        if callable(self.forcing):
            return self.forcing(n)
        return self.forcing

    def evaluate(self, n):
        if n < 0:
            raise ValueError("n must be >= 0")

        cache = {}

        def solve(k):
            if k < self.order:
                return self.initial[k]

            if k in cache:
                return cache[k]

            value = self._forcing(k)

            for index, coefficient in enumerate(self.coefficients):
                value += coefficient * solve(k - index - 1)

            cache[k] = value
            return value

        return solve(n)

    def sequence(self, limit):
        if limit < 0:
            raise ValueError("limit must be >= 0")

        return tuple(
            self.evaluate(n)
            for n in range(limit + 1)
        )

    def ratio_sequence(self, limit):
        values = self.sequence(limit)

        ratios = []
        for left, right in zip(values, values[1:]):
            if left == 0:
                ratios.append(None)
            else:
                ratios.append(right / left)

        return tuple(ratios)

    def signature(self):
        return {
            "name": self.name,
            "order": self.order,
            "initial": self.initial,
            "coefficients": self.coefficients,
        }


def fibonacci_recurrence():
    return SEARecurrence(
        name="fibonacci",
        initial=(0, 1),
        coefficients=(1, 1),
        forcing=0,
    )


def binary_tree_recurrence():
    return SEARecurrence(
        name="binary_tree",
        initial=(1,),
        coefficients=(2,),
        forcing=1,
    )
