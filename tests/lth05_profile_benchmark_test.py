import unittest

from src.lth05.benchmark import benchmark_vm
from src.lth05.runner import LTH05Runner


class LTH05ProfileBenchmarkTest(unittest.TestCase):
    def test_profile(self):
        source = "value = 2 + 3 * 4"

        result = LTH05Runner().run(
            source,
            trace=True,
        )

        self.assertEqual(
            result.values["value"],
            14,
        )
        self.assertGreater(
            result.profile.instruction_count,
            0,
        )
        self.assertTrue(
            isinstance(result.profile.trace, list)
        )

    def test_benchmark(self):
        runner = LTH05Runner()
        source = "value = 10 * 20"

        result = benchmark_vm(
            runner,
            source,
            iterations=10,
            warmup=2,
        )

        self.assertEqual(result.iterations, 10)
        self.assertGreaterEqual(
            result.seconds,
            0.0,
        )
        self.assertGreater(
            result.nanoseconds_per_run,
            0.0,
        )


if __name__ == "__main__":
    unittest.main()
