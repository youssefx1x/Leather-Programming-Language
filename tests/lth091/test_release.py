import tempfile
import unittest
from pathlib import Path

from src.lth091 import __version__
from src.lth091.runtime import (
    LTHRuntime,
    LTHError,
    LTHModuleError,
)
from src.lth091.runner import LeatherRunner
from src.lth091.performance import PerformanceTransparency
from src.lth091.compatibility import CompatibilityGuard
from src.lth091.bootstrap import RustBootstrap


class TestLTH091Release(unittest.TestCase):

    def test_version(self):
        self.assertEqual(__version__, "0.9.1")

    def test_runtime(self):
        runtime = LTHRuntime()
        report = runtime.execute("hello")

        self.assertTrue(report.success)
        self.assertEqual(report.output, "hello")
        self.assertGreaterEqual(report.elapsed_ns, 0)

    def test_runner_text(self):
        runner = LeatherRunner()
        report = runner.run_text("Leather")

        self.assertTrue(report.success)
        self.assertEqual(report.output, "Leather")
        self.assertEqual(runner.version(), "0.9.1")

    def test_runner_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hello.lth"
            path.write_text("hello")

            report = LeatherRunner().run_file(path)

            self.assertTrue(report.success)
            self.assertEqual(report.output, "hello")

    def test_missing_file_is_native_error(self):
        with self.assertRaises(Exception):
            LeatherRunner().run_file(
                "/definitely/not/a/real/lth/file.lth"
            )

    def test_module_loader(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "module.py"
            path.write_text("value = 42\n")

            module = LTHRuntime().modules.load(path)

            self.assertEqual(module.value, 42)

    def test_module_error(self):
        with self.assertRaises(LTHModuleError):
            LTHRuntime().modules.load(
                "/definitely/not/a/module.py"
            )

    def test_performance_transparency(self):
        perf = PerformanceTransparency()

        result = perf.measure(
            "addition",
            lambda: 2 + 3,
            calls=100,
        )

        snapshot = perf.snapshot("addition")

        self.assertEqual(result, 5)
        self.assertIsNotNone(snapshot)
        self.assertEqual(snapshot.calls, 100)
        self.assertGreaterEqual(snapshot.elapsed_ns, 0)

    def test_compatibility_contract(self):
        namespace = {
            "value": object(),
            "rule": object(),
            "base": object(),
            "flow": object(),
            "system": object(),
        }

        guard = CompatibilityGuard()

        self.assertTrue(guard.passed(namespace))
        self.assertEqual(len(guard.check_concepts(namespace)), 5)

    def test_rust_bootstrap(self):
        result = RustBootstrap().check()

        self.assertTrue(result.available)
        self.assertEqual(result.compiler, "rustc")
        self.assertIn("rustc", result.version)


if __name__ == "__main__":
    unittest.main()
