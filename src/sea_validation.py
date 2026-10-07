from dataclasses import dataclass


@dataclass(frozen=True)
class SEAViolation:
    code: str
    message: str


@dataclass(frozen=True)
class SEAValidationReport:
    valid: bool
    violations: tuple = ()

    @property
    def count(self):
        return len(self.violations)


def validate_search_result(result):
    violations = []

    if result.generated < 0:
        violations.append(
            SEAViolation(
                "SEARCH-001",
                "generated count must be non-negative",
            )
        )

    if result.expanded < 0:
        violations.append(
            SEAViolation(
                "SEARCH-002",
                "expanded count must be non-negative",
            )
        )

    if result.unique_states < 0:
        violations.append(
            SEAViolation(
                "SEARCH-003",
                "unique state count must be non-negative",
            )
        )

    if result.depth < -1:
        violations.append(
            SEAViolation(
                "SEARCH-004",
                "depth cannot be below -1",
            )
        )

    return SEAValidationReport(
        valid=not violations,
        violations=tuple(violations),
    )


def validate_recurrence(recurrence):
    violations = []

    if recurrence.order <= 0:
        violations.append(
            SEAViolation(
                "REC-001",
                "recurrence order must be positive",
            )
        )

    if len(recurrence.initial) != len(
        recurrence.coefficients
    ):
        violations.append(
            SEAViolation(
                "REC-002",
                "initial and coefficient lengths differ",
            )
        )

    return SEAValidationReport(
        valid=not violations,
        violations=tuple(violations),
    )


def validate_graph(graph):
    violations = []

    for source, target in graph.edges():
        if not graph.has_node(source):
            violations.append(
                SEAViolation(
                    "GRAPH-001",
                    "edge source missing from node set",
                )
            )

        if not graph.has_node(target):
            violations.append(
                SEAViolation(
                    "GRAPH-002",
                    "edge target missing from node set",
                )
            )

    return SEAValidationReport(
        valid=not violations,
        violations=tuple(violations),
    )
