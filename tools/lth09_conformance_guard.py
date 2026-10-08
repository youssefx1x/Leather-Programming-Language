from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main():
    result = subprocess.run(
        ["python", "tools/lth08_run_all.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    print(result.stdout, end="")
    print(result.stderr, end="")

    if result.returncode != 0:
        raise SystemExit("LTH 0.8 semantic guard FAILED")

    required = (
        "LTH 0.8 CONFORMANCE: VERIFIED",
        "Python: 18/18 PASS",
        "C++: 18/18 PASS",
        "Rust: 18/18 PASS",
        "CROSS-MATCH: 18/18",
    )

    for marker in required:
        if marker not in result.stdout:
            raise SystemExit(
                f"semantic guard missing marker: {marker}"
            )

    print("LTH 0.9 SEMANTIC GUARD: PASS")


if __name__ == "__main__":
    main()
