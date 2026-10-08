#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/conformance/lth08_cases.tsv"


def run(command):
    start = time.perf_counter()
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    elapsed = (time.perf_counter() - start) * 1000.0

    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="")
        raise SystemExit(
            f"COMMAND FAILED ({result.returncode}): {' '.join(command)}"
        )

    return result.stdout.strip().splitlines(), elapsed


def expected_cases():
    rows = []

    for line in CASES.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue

        fields = line.split("\t")

        if len(fields) != 6:
            raise SystemExit("invalid conformance corpus")

        rows.append((fields[0], fields[5]))

    return rows


def compare(name, actual_lines, expected):
    actual = {}

    for line in actual_lines:
        parts = line.split("\t", 1)

        if len(parts) != 2:
            raise SystemExit(f"{name}: malformed output: {line}")

        actual[parts[0]] = parts[1]

    expected_map = dict(expected)

    if set(actual) != set(expected_map):
        raise SystemExit(
            f"{name}: case-id mismatch"
        )

    failures = []

    for case_id, expected_value in expected:
        if actual[case_id] != expected_value:
            failures.append(
                f"{case_id}: expected {expected_value}, got {actual[case_id]}"
            )

    if failures:
        print(f"{name}: FAIL")
        for item in failures:
            print(item)
        raise SystemExit(1)

    return actual


def main():
    expected = expected_cases()

    contract_output, _ = run(
        ["python", "tools/lth08_contract_check.py"]
    )

    if "LTH 0.8 CONTRACT CHECK: PASS" not in contract_output:
        raise SystemExit("contract check failed")

    results = {}

    python_output, python_ms = run(
        [
            "python",
            "tests/conformance/lth08_python_probe.py",
            str(CASES),
        ]
    )
    results["Python"] = compare(
        "Python",
        python_output,
        expected,
    )

    compiler = (
        shutil.which("c++")
        or shutil.which("clang++")
        or shutil.which("g++")
    )

    if not compiler:
        raise SystemExit("C++ compiler not found")

    rustc = shutil.which("rustc")

    if not rustc:
        raise SystemExit("rustc not found")

    with tempfile.TemporaryDirectory() as temp:
        cpp_binary = Path(temp) / "lth08_cpp_probe"
        rust_binary = Path(temp) / "lth08_rust_probe"

        run(
            [
                compiler,
                "-std=c++17",
                "-O2",
                "-Wall",
                "-Wextra",
                "-Werror",
                "tests/conformance/lth08_cpp_probe.cpp",
                "-o",
                str(cpp_binary),
            ]
        )

        run(
            [
                rustc,
                "--edition=2021",
                "-O",
                "-D",
                "warnings",
                "tests/conformance/lth08_rust_probe.rs",
                "-o",
                str(rust_binary),
            ]
        )

        cpp_output, cpp_ms = run(
            [str(cpp_binary), str(CASES)]
        )

        rust_output, rust_ms = run(
            [str(rust_binary), str(CASES)]
        )

    results["C++"] = compare(
        "C++",
        cpp_output,
        expected,
    )

    results["Rust"] = compare(
        "Rust",
        rust_output,
        expected,
    )

    ids = [case_id for case_id, _ in expected]

    for case_id in ids:
        values = [
            results["Python"][case_id],
            results["C++"][case_id],
            results["Rust"][case_id],
        ]

        if not (values[0] == values[1] == values[2]):
            raise SystemExit(
                f"CROSS-MATCH FAIL: {case_id}: {values}"
            )

    matrix = ROOT / "tests/conformance/lth08_matrix.tsv"

    matrix.write_text(
        "implementation\tcases\tpassed\tstatus\twall_ms\n"
        f"Python\t{len(expected)}\t{len(expected)}\tPASS\t{python_ms:.3f}\n"
        f"C++\t{len(expected)}\t{len(expected)}\tPASS\t{cpp_ms:.3f}\n"
        f"Rust\t{len(expected)}\t{len(expected)}\tPASS\t{rust_ms:.3f}\n"
        f"Cross-Match\t{len(expected)}\t{len(expected)}\tPASS\t-\n",
        encoding="utf-8",
    )

    print()
    print("========================================")
    print("LTH 0.8 CONFORMANCE: VERIFIED")
    print(f"CASES: {len(expected)}")
    print(f"Python: {len(expected)}/{len(expected)} PASS")
    print(f"C++: {len(expected)}/{len(expected)} PASS")
    print(f"Rust: {len(expected)}/{len(expected)} PASS")
    print(f"CROSS-MATCH: {len(expected)}/{len(expected)}")
    print("STATUS: PASS")
    print("========================================")


if __name__ == "__main__":
    main()
