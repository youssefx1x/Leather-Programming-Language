from dataclasses import dataclass


@dataclass(frozen=True)
class CompatibilityResult:
    name: str
    passed: bool
    detail: str


class CompatibilityGuard:
    """
    Guards the stable release against the frozen LTH 0.1 contract.

    The guard checks the foundational concepts without replacing
    or modifying the 0.1 implementation.
    """

    REQUIRED_CONCEPTS = (
        "value",
        "rule",
        "base",
        "flow",
        "system",
    )

    def check_concepts(self, namespace):
        results = []

        for name in self.REQUIRED_CONCEPTS:
            present = name in namespace
            results.append(
                CompatibilityResult(
                    name=name,
                    passed=present,
                    detail="present" if present else "missing",
                )
            )

        return results

    def passed(self, namespace):
        return all(r.passed for r in self.check_concepts(namespace))
