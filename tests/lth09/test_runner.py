import unittest

from src.lth09.engine import AcceleratedEngine
from src.lth09.profiler import HotPathProfiler


class LTH09Tests(unittest.TestCase):

    def test_integer_fast_path(self):
        engine = AcceleratedEngine()
        self.assertEqual(engine.add(2, 3), 5)
        self.assertEqual(engine.stats.fast_path_hits, 1)

    def test_float_semantics(self):
        engine = AcceleratedEngine()
        self.assertLess(abs(engine.add(2, 0.5) - 2.5), 1e-12)

    def test_string_semantics(self):
        engine = AcceleratedEngine()
        self.assertEqual(
            engine.add("hello ", "world"),
            "hello world",
        )

    def test_cache_path(self):
        engine = AcceleratedEngine()

        first = engine.add(2.5, 0.5)
        second = engine.add(2.5, 0.5)

        self.assertEqual(first, 3.0)
        self.assertEqual(second, 3.0)
        self.assertEqual(engine.stats.cache_hits, 1)

    def test_bool_is_not_integer_fast_path(self):
        engine = AcceleratedEngine()

        result = engine.add(True, 2)

        self.assertEqual(result, 3)
        self.assertEqual(engine.stats.fast_path_hits, 0)

    def test_profiler(self):
        profiler = HotPathProfiler()

        self.assertEqual(
            profiler.measure("add", lambda: 2 + 3),
            5,
        )

        profiler.measure("add", lambda: 4 + 5)
        profiler.measure("scan", lambda: sum(range(10)))

        summary = profiler.summary()

        self.assertEqual(len(summary), 2)
        self.assertTrue(
            all(item["calls"] > 0 for item in summary)
        )


if __name__ == "__main__":
    unittest.main()
