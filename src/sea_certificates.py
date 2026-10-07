from dataclasses import dataclass


@dataclass(frozen=True)
class SEACondition:
    name: str
    satisfied: bool
    detail: str = ""


@dataclass(frozen=True)
class SEAOptimizationCertificate:
    name: str
    source_result: object
    target_result: object
    semantic_equivalence: bool
    conditions: tuple = ()

    @property
    def conditions_valid(self):
        return all(
            condition.satisfied
            for condition in self.conditions
        )

    @property
    def valid(self):
        return (
            self.semantic_equivalence
            and self.conditions_valid
        )

    def summary(self):
        return {
            "name": self.name,
            "semantic_equivalence":
                self.semantic_equivalence,
            "conditions_valid":
                self.conditions_valid,
            "valid": self.valid,
            "conditions": tuple(
                condition.name
                for condition in self.conditions
                if condition.satisfied
            ),
        }


def certify_optimization(
    name,
    source_result,
    target_result,
    semantic_equivalence,
    conditions=(),
):
    return SEAOptimizationCertificate(
        name=name,
        source_result=source_result,
        target_result=target_result,
        semantic_equivalence=semantic_equivalence,
        conditions=tuple(conditions),
    )
