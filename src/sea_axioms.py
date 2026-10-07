from dataclasses import dataclass


@dataclass(frozen=True)
class SEAAxiom:
    code: str
    name: str
    statement: str


SEA_AXIOMS = (
    SEAAxiom(
        "SEA-A01",
        "Regular Conservativity",
        "Regular arithmetic must preserve its ordinary result "
        "when no exceptional rule is triggered.",
    ),
    SEAAxiom(
        "SEA-A02",
        "Exceptional Separation",
        "Exceptional states are distinct semantic states and "
        "must not be silently coerced into regular values.",
    ),
    SEAAxiom(
        "SEA-A03",
        "Context Preservation",
        "An exceptional state retains the operation and operand "
        "context that produced it.",
    ),
    SEAAxiom(
        "SEA-A04",
        "Explicit Transition",
        "A state change occurs through an explicit operation/rule "
        "transition.",
    ),
    SEAAxiom(
        "SEA-A05",
        "Complexity Compositionality",
        "A composed computation has a derived complexity state.",
    ),
    SEAAxiom(
        "SEA-A06",
        "Meaning Preservation",
        "A valid optimization must preserve the intended semantics.",
    ),
    SEAAxiom(
        "SEA-A07",
        "Complexity Nonnegativity",
        "Measured complexity dimensions cannot be negative.",
    ),
    SEAAxiom(
        "SEA-A08",
        "No Unjustified Collapse",
        "An exceptional state may only become a regular value "
        "through an explicit validated rule.",
    ),
    SEAAxiom(
        "SEA-A09",
        "Representation Independence",
        "Internal representation may change without changing "
        "the mathematical meaning.",
    ),
    SEAAxiom(
        "SEA-A10",
        "Complexity Awareness",
        "A SEA computation may carry symbolic complexity even "
        "when direct enumeration is infeasible.",
    ),
)


def axiom_codes():
    return tuple(
        axiom.code
        for axiom in SEA_AXIOMS
    )


def get_axiom(code):
    for axiom in SEA_AXIOMS:
        if axiom.code == code:
            return axiom

    raise KeyError(
        f"unknown SEA axiom '{code}'"
    )


def validate_axiom_set():
    codes = axiom_codes()

    if len(codes) != len(set(codes)):
        raise ValueError(
            "duplicate SEA axiom code"
        )

    return True
