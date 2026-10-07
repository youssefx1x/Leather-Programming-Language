from pathlib import Path
import runpy
import sys


TESTS = (
    "tests/lth_04_compile_test.py",
    "tests/lth_04_optimizer_test.py",
    "tests/lth_04_vm_test.py",
    "tests/lth_04_cache_test.py",
    "tests/lth_04_language_test.py",
    "tests/lth_04_equivalence_test.py",
    "tests/lth_04_trace_test.py",
    "tests/lth_04_benchmark_test.py",
)


def main():
    root = Path(__file__).resolve().parents[1]

    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    for filename in TESTS:
        runpy.run_path(
            str(root / filename),
            run_name="__main__",
        )

    print(
        "LTH 0.4 FINAL REGRESSION: "
        f"{len(TESTS)}/{len(TESTS)} PASS"
    )


if __name__ == "__main__":
    main()
