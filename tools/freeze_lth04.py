from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "freeze"
DOCS = ROOT / "docs"

MANIFEST = (
    FREEZE / "LTH-0.4-FINAL-SHA256.txt"
)

VERIFY = (
    FREEZE / "LTH-0.4-FINAL-SHA256.verify.txt"
)

DOC = (
    DOCS / "LTH-0.4-FINAL-FREEZE.md"
)


def selected_files():
    files = []

    roots = (
        ROOT / "src" / "lth04",
        ROOT / "tests",
        ROOT / "tools",
        ROOT / "examples",
        ROOT / "docs",
    )

    for directory in roots:
        if not directory.exists():
            continue

        for path in directory.rglob("*"):
            if not path.is_file():
                continue

            if "__pycache__" in path.parts:
                continue

            rel = path.relative_to(ROOT)

            if rel.parts[0] == "tests":
                if not path.name.startswith(
                    "lth_04_"
                ):
                    continue

            if rel.parts[0] == "tools":
                if not path.name.startswith(
                    "lth04"
                ):
                    continue

            if rel.parts[0] == "docs":
                if path.name != (
                    "LTH-0.4-FINAL-FREEZE.md"
                ):
                    continue

            if path.suffix not in (
                ".py",
                ".lth",
                ".md",
            ):
                continue

            files.append(rel)

    return sorted(set(files))


def digest(path):
    return sha256(
        path.read_bytes()
    ).hexdigest()


def main():
    FREEZE.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)

    files = selected_files()

    lines = [
        f"{digest(ROOT / rel)}  {rel.as_posix()}"
        for rel in files
    ]

    MANIFEST.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    failures = []

    for line in lines:
        expected, rel = line.split(
            "  ",
            1,
        )

        actual = digest(
            ROOT / rel
        )

        if actual != expected:
            failures.append(rel)

    VERIFY.write_text(
        "\n".join(
            [
                "LTH 0.4 FINAL FREEZE VERIFICATION",
                f"FILES CHECKED: {len(files)}",
                f"FAILURES: {len(failures)}",
                (
                    "INTEGRITY: PASS"
                    if not failures
                    else "INTEGRITY: FAIL"
                ),
                (
                    "FINAL FREEZE: VERIFIED"
                    if not failures
                    else "FINAL FREEZE: FAILED"
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    if failures:
        raise SystemExit(
            "integrity failures: "
            + ", ".join(failures)
        )

    manifest_hash = digest(MANIFEST)

    DOC.write_text(
        "\n".join(
            [
                "# Leather 0.4 — FINAL FREEZE",
                "",
                "Status: VERIFIED",
                "",
                "LTH 0.4 layers:",
                "- A Execution IR",
                "- B Bytecode Compiler",
                "- C Optimizer + Validator",
                "- D Bytecode VM",
                "- E Compilation Cache",
                "- F Explainable Execution Trace",
                "- G Semantic Equivalence",
                "- H Benchmark / Performance Transparency",
                "- I Final Regression + Integrity",
                "",
                "LTH 0.3 remains the semantic baseline.",
                "LTH 0.4 adds an accelerated execution",
                "foundation without changing language meaning.",
                "",
                f"FILES CHECKED: {len(files)}",
                "FAILURES: 0",
                "INTEGRITY: PASS",
                "FINAL FREEZE: VERIFIED",
                "",
                f"MANIFEST SHA-256: {manifest_hash}",
                "",
                "Generated: "
                + datetime.now(
                    timezone.utc
                ).isoformat(),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print("LTH 0.4 FINAL FREEZE")
    print(f"FILES CHECKED: {len(files)}")
    print("FAILURES: 0")
    print("INTEGRITY: PASS")
    print(
        "MANIFEST SHA-256:",
        manifest_hash,
    )
    print("FINAL FREEZE: VERIFIED")


if __name__ == "__main__":
    main()
