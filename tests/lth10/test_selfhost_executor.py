import unittest
from pathlib import Path

from src.lth10.selfhost.executor import LeatherSelfHostExecutor


class TestSelfHostExecutor(unittest.TestCase):

    def setUp(self):
        self.executor = LeatherSelfHostExecutor()
        self.source = Path("src/lth10/selfhost/core.lth")

    def test_load(self):
        source = self.executor.load(self.source)

        self.assertIn("rule", source)
        self.assertIn("system", source)

    def test_inspect(self):
        report = self.executor.inspect(self.source)

        self.assertEqual(report["version"], "1.0")
        self.assertTrue(report["valid"])
        self.assertGreater(report["lines"], 0)

    def test_all_core_constructs(self):
        report = self.executor.inspect(self.source)

        expected = {
            "value",
            "rule",
            "base",
            "flow",
            "system",
        }

        self.assertEqual(
            set(report["constructs"].keys()),
            expected,
        )

        self.assertTrue(
            all(report["constructs"].values())
        )

    def test_execute_boundary(self):
        report = self.executor.execute(self.source)

        self.assertTrue(report["valid"])
        self.assertEqual(report["version"], "1.0")


if __name__ == "__main__":
    unittest.main()
