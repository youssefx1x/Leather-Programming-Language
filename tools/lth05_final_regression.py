import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


TEST_MODULES = [
    "tests.lth05_bytecode_test",
    "tests.lth05_vm_test",
    "tests.lth05_specialization_test",
    "tests.lth05_optimizer_test",
    "tests.lth05_language_test",
    "tests.lth05_equivalence_test",
    "tests.lth05_profile_benchmark_test",
    "tests.lth05_integration_test",
]


def main():
    suite = unittest.TestSuite()

    for module in TEST_MODULES:
        suite.addTests(
            unittest.defaultTestLoader.loadTestsFromName(module)
        )

    result = unittest.TextTestRunner(
        verbosity=1,
    ).run(suite)

    print()
    print("LTH 0.5 FINAL REGRESSION")
    print(f"TESTS RUN: {result.testsRun}")
    print(f"FAILURES: {len(result.failures)}")
    print(f"ERRORS: {len(result.errors)}")

    if result.wasSuccessful():
        print("LTH 0.5 REGRESSION: PASS")
        return 0

    print("LTH 0.5 REGRESSION: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
