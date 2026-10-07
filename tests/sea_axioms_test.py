from src.sea_axioms import (
    SEA_AXIOMS,
    axiom_codes,
    get_axiom,
    validate_axiom_set,
)


def main():
    assert len(SEA_AXIOMS) == 10
    assert validate_axiom_set()

    codes = axiom_codes()

    assert codes[0] == "SEA-A01"
    assert codes[-1] == "SEA-A10"

    axiom = get_axiom("SEA-A06")

    assert axiom.name == "Meaning Preservation"
    assert "semantics" in axiom.statement.lower()

    print("SEA 0.1 AXIOM SYSTEM: PASS")


if __name__ == "__main__":
    main()
