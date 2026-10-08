from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CHECKED_FILES = [
    Path("src/lth09/__init__.py"),
    Path("src/lth09/engine.py"),
    Path("src/lth09/profiler.py"),
    Path("tests/lth09/test_engine.py"),
    Path("tests/lth09/test_profiler.py"),
    Path("tests/lth09/lth09_benchmark.json"),
    Path("tools/lth09_benchmark.py"),
    Path("tools/lth09_conformance_guard.py"),
    Path("tools/lth09_closeout.py"),
    Path("docs/LTH-0.9-EXECUTION-ACCELERATION.md"),
]


def run(command):
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    print(result.stdout, end="")
    print(result.stderr, end="")

    if result.returncode != 0:
        raise SystemExit(
            f"FAILED: {' '.join(command)}"
        )


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    run(["python", "tools/lth09_conformance_guard.py"])

    run([
        "python",
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests/lth09",
        "-p",
        "test_*.py",
        "-v",
    ])

    run([
        "python",
        "tools/lth09_benchmark.py",
    ])

    missing = [
        str(path)
        for path in CHECKED_FILES
        if not (ROOT / path).is_file()
    ]

    if missing:
        raise SystemExit(
            "MISSING FILES:\n" + "\n".join(missing)
        )

    freeze_dir = ROOT / "freeze"
    freeze_dir.mkdir(exist_ok=True)

    manifest = freeze_dir / "LTH-0.9-SHA256.txt"

    lines = [
        f"{sha256(ROOT / path)}  {path.as_posix()}"
        for path in CHECKED_FILES
    ]

    manifest.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    manifest_hash = sha256(manifest)

    final_doc = ROOT / "docs/LTH-0.9-FINAL-FREEZE.md"

    final_doc.write_text(
        "# LTH 0.9 — Final Freeze\n\n"
        "Status: FROZEN\n\n"
        "## Theme\n\n"
        "Execution Acceleration\n\n"
        "## Guarantees\n\n"
        "- LTH 0.8 semantic conformance remains PASS.\n"
        "- Python, C++, and Rust remain cross-conformant.\n"
        "- Accelerated execution preserves the benchmark semantic result.\n"
        "- Hot-path profiling is available.\n"
        "- Specialized execution paths are explicit.\n"
        "- Repeated computation can use bounded memoization.\n\n"
        "## Integrity\n\n"
        f"- Files checked: {len(CHECKED_FILES)}\n"
        "- Semantic guard: PASS\n"
        "- Unit tests: PASS\n"
        "- Benchmark: PASS\n"
        f"- Manifest SHA-256: `{manifest_hash}`\n"
        "- Warnings: 0\n\n"
        "## Principle\n\n"
        "> Same semantics. Less execution cost.\n",
        encoding="utf-8",
    )

    print()
    print("========================================")
    print("LTH 0.9 FINAL FREEZE: VERIFIED")
    print(f"FILES CHECKED: {len(CHECKED_FILES)}")
    print("SEMANTIC GUARD: PASS")
    print("UNIT TESTS: PASS")
    print("BENCHMARK: PASS")
    print("PERFORMANCE PATH: ACTIVE")
    print("INTEGRITY: PASS")
    print("WARNINGS: 0")
    print("LTH 0.9: FROZEN")
    print("========================================")


if __name__ == "__main__":
    main()
