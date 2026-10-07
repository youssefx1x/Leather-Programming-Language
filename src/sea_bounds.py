from dataclasses import dataclass
import math

from src.sea_complexity import ComplexityExpr
from src.sea_growth import SEAAsymptoticClaim, SEAAsymptoticKind


@dataclass(frozen=True)
class SEABound:
    kind: SEAAsymptoticKind
    function: ComplexityExpr
    bound: ComplexityExpr
    constant_factor: float = 1.0
    threshold: int = 1
    basis: str = "sample_validation"

    def evaluate_pair(self, n):
        environment = {"n": n}
        value = self.function.evaluate(environment)
        bound = self.bound.evaluate(environment)
        return value, self.constant_factor * bound

    def holds(self, samples):
        for n in samples:
            if n < self.threshold:
                continue

            value, bound = self.evaluate_pair(n)

            if self.kind == SEAAsymptoticKind.O:
                if value > bound:
                    return False

            elif self.kind == SEAAsymptoticKind.OMEGA:
                if value < bound:
                    return False

            elif self.kind == SEAAsymptoticKind.THETA:
                if value > bound or value < bound / 2:
                    return False

            elif self.kind == SEAAsymptoticKind.EXACT:
                if not math.isclose(
                    value,
                    bound,
                    rel_tol=1e-12,
                    abs_tol=1e-12,
                ):
                    return False

        return True

    def claim(self):
        return SEAAsymptoticClaim(
            kind=self.kind,
            function=self.function,
            reference=self.bound,
            statement=self.render_statement(),
        )

    def render_statement(self):
        if self.kind == SEAAsymptoticKind.O:
            return (
                "function is bounded above by the supplied "
                "reference on the validation domain"
            )

        if self.kind == SEAAsymptoticKind.OMEGA:
            return (
                "function is bounded below by the supplied "
                "reference on the validation domain"
            )

        if self.kind == SEAAsymptoticKind.THETA:
            return (
                "function is bounded within the supplied "
                "constant band on the validation domain"
            )

        return (
            "function matches the supplied reference "
            "on the validation domain"
        )


@dataclass(frozen=True)
class SEABoundCertificate:
    bound: SEABound
    samples: tuple
    validated: bool

    @property
    def status(self):
        return "validated" if self.validated else "rejected"

    def summary(self):
        return {
            "kind": self.bound.kind.value,
            "status": self.status,
            "samples": self.samples,
            "basis": self.bound.basis,
        }


def validate_bound(bound, samples=(10, 20, 50, 100)):
    samples = tuple(samples)

    return SEABoundCertificate(
        bound=bound,
        samples=samples,
        validated=bound.holds(samples),
    )
