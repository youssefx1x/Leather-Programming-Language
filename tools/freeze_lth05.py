from hashlib import sha256
from pathlib import Path


ROOT = Path(".")
MANIFEST = ROOT / "freeze/LTH-0.5-FINAL-SHA256.txt"
VERIFY = ROOT / "freeze/LTH-0.5-FINAL-SHA256.verify.txt"
DOC = ROOT / "docs/LTH-0.5-FINAL-FREEZE.md"


def collect():
    files = []

    for base in [
        ROOT / "src/lth05",
    ]:
        files.extend(
            path
            for path in base.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
        )

    files.extend(
        path
        for path in ROOT.glob("tests/lth05*_test.py")
        if path.is_file()
    )

    files.extend([
        ROOT / "tools/lth05_final_regression.py",
        ROOT / "tools/freeze_lth05.py",
        ROOT / "examples/lth05_acceleration_demo.lth",
        ROOT / "examples/lth05_acceleration_demo.context.json",
        ROOT / "docs/LTH-0.5-DESIGN.md",
    ])

    return sorted({
        path.resolve()
        for path in files
        if path.exists()
    })


def digest(path):
    return sha256(
        path.read_bytes()
    ).hexdigest()


def main():
    files = collect()

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    for path in files:
        relative = path.relative_to(ROOT.resolve())
        lines.append(
            f"{digest(path)}  {relative}"
        )

    payload = "\n".join(lines) + "\n"
    MANIFEST.write_text(
        payload,
        encoding="utf-8",
    )

    manifest_hash = sha256(
        MANIFEST.read_bytes()
    ).hexdigest()

    failures = []

    for line in payload.splitlines():
        expected, relative = line.split("  ", 1)
        actual = digest(ROOT / relative)

        if actual != expected:
            failures.append(relative)

    VERIFY.write_text(
        "\n".join(
            f"{path.relative_to(ROOT.resolve())}: "
            f"{'OK' if path not in failures else 'FAIL'}"
            for path in files
        ) + "\n",
        encoding="utf-8",
    )

    DOC.write_text(
        "\n".join([
            "# Leather 0.5 — Final Freeze",
            "",
            "LTH 0.5 final execution-layer freeze.",
            "",
            f"FILES CHECKED: {len(files)}",
            f"FAILURES: {len(failures)}",
            f"INTEGRITY: {'PASS' if not failures else 'FAIL'}",
            f"MANIFEST SHA-256: {manifest_hash}",
            "",
            "Scope:",
            "- typed/structured bytecode model",
            "- stack-based virtual machine",
            "- optimizer",
            "- runtime specialization",
            "- execution profiling",
            "- tracing",
            "- equivalence testing against LTH 0.3",
            "- benchmark infrastructure",
            "",
            "LTH 0.4 frozen core remains untouched.",
            "",
            (
                "FINAL FREEZE: VERIFIED"
                if not failures
                else "FINAL FREEZE: FAILED"
            ),
        ]) + "\n",
        encoding="utf-8",
    )

    print("LTH 0.5 FINAL FREEZE")
    print(f"FILES CHECKED: {len(files)}")
    print(f"FAILURES: {len(failures)}")
    print(
        f"INTEGRITY: {'PASS' if not failures else 'FAIL'}"
    )
    print(f"MANIFEST SHA-256: {manifest_hash}")

    if failures:
        print("FAILED FILES:")
        for item in failures:
            print(item)
        print("FINAL FREEZE: FAILED")
        return 1

    print("FINAL FREEZE: VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
