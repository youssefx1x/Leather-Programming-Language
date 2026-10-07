from dataclasses import dataclass
from enum import Enum


class SEAProofStatus(Enum):
    VALIDATED = "validated"
    REJECTED = "rejected"
    CONDITIONAL = "conditional"


@dataclass(frozen=True)
class SEAProofStep:
    name: str
    statement: str
    justified: bool
    evidence: str = ""


@dataclass(frozen=True)
class SEAMeaningClaim:
    source: object
    target: object
    equivalent: bool
    basis: str


@dataclass(frozen=True)
class SEAComplexityClaim:
    source_cost: float
    target_cost: float
    improved: bool


@dataclass(frozen=True)
class SEACertificate:
    name: str
    meaning_claim: SEAMeaningClaim
    complexity_claim: SEAComplexityClaim
    steps: tuple = ()

    @property
    def status(self):
        if not self.meaning_claim.equivalent:
            return SEAProofStatus.REJECTED

        if not self.complexity_claim.improved:
            return SEAProofStatus.CONDITIONAL

        if not all(
            step.justified
            for step in self.steps
        ):
            return SEAProofStatus.CONDITIONAL

        return SEAProofStatus.VALIDATED

    def summary(self):
        return {
            "name": self.name,
            "status": self.status.value,
            "meaning_equivalent":
                self.meaning_claim.equivalent,
            "complexity_improved":
                self.complexity_claim.improved,
            "steps": len(self.steps),
        }


def certify(
    name,
    meaning_claim,
    complexity_claim,
    steps=(),
):
    return SEACertificate(
        name=name,
        meaning_claim=meaning_claim,
        complexity_claim=complexity_claim,
        steps=tuple(steps),
    )
