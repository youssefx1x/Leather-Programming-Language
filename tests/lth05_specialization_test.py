import unittest

from src.lth05.profiler import ExecutionProfile
from src.lth05.specialized import SpecializationCache


class LTH05SpecializationTest(unittest.TestCase):
    def test_specialization_cache(self):
        cache = SpecializationCache()
        profile = ExecutionProfile()

        self.assertEqual(
            cache.execute("+", 10, 20, profile),
            30,
        )

        self.assertEqual(
            cache.execute("+", 11, 21, profile),
            32,
        )

        self.assertGreaterEqual(
            profile.specialization_misses,
            1,
        )
        self.assertGreaterEqual(
            profile.specialization_hits,
            1,
        )
        self.assertGreaterEqual(
            cache.size(),
            1,
        )


if __name__ == "__main__":
    unittest.main()
