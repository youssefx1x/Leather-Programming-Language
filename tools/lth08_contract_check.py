from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "LTH-0.8-SEMANTIC-CONTRACT.md"
CASES = ROOT / "tests" / "conformance" / "lth08_cases.tsv"

VALID_CATEGORIES = {
    "numeric",
    "equality",
    "truth",
    "boolean",
    "string",
    "collection",
    "error",
}

VALID_VALUE_PREFIXES = {
    "None",
    "Bool(",
    "Int(",
    "Float(",
    "Str(",
    "List(",
    "Map(",
    "Error(",
}

def validate():
    if not DOC.is_file():
        raise SystemExit("FAIL: semantic contract missing")

    if not CASES.is_file():
        raise SystemExit("FAIL: conformance case file missing")

    doc = DOC.read_text(encoding="utf-8")
    required = (
        "LTH 0.8 Semantic Contract",
        "One Language Semantics.",
        "Multiple Implementations.",
        "One Canonical Behavior.",
    )

    for item in required:
        if item not in doc:
            raise SystemExit(f"FAIL: contract marker missing: {item}")

    seen = set()
    count = 0

    for lineno, raw in enumerate(CASES.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()

        if not line or line.startswith("#"):
            continue

        fields = raw.split("\t")
        if len(fields) != 6:
            raise SystemExit(
                f"FAIL: line {lineno}: expected 6 tab-separated fields"
            )

        case_id, category, op, left, right, expected = fields

        if case_id in seen:
            raise SystemExit(f"FAIL: duplicate case id: {case_id}")

        if not case_id.startswith("LTH08-"):
            raise SystemExit(f"FAIL: invalid case id: {case_id}")

        if category not in VALID_CATEGORIES:
            raise SystemExit(
                f"FAIL: unknown category '{category}' at line {lineno}"
            )

        if not op:
            raise SystemExit(f"FAIL: empty operation at line {lineno}")

        for label, value in (("left", left), ("right", right), ("expected", expected)):
            if value == "-" and label != "right":
                raise SystemExit(
                    f"FAIL: invalid '-' in {label} at line {lineno}"
                )

        if not any(expected.startswith(prefix) for prefix in VALID_VALUE_PREFIXES):
            raise SystemExit(
                f"FAIL: unsupported expected value '{expected}' at line {lineno}"
            )

        seen.add(case_id)
        count += 1

    if count == 0:
        raise SystemExit("FAIL: no conformance cases found")

    print("LTH 0.8 CONTRACT CHECK: PASS")
    print(f"CONFORMANCE CASES: {count}")
    print("CONTRACT MARKERS: PASS")
    print("SCHEMA: PASS")


if __name__ == "__main__":
    validate()
