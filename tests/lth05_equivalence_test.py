import unittest

from src.lth05.equivalence import run_equivalence


class LTH05EquivalenceTest(unittest.TestCase):
    def test_reference_equivalence(self):
        source = """
price = 150.5
rule discount when customer.vip -> price *= 0.9
"""

        result = run_equivalence(
            source,
            context={
                "customer": {
                    "vip": True,
                }
            },
        )

        self.assertTrue(result["equivalent"])
        self.assertAlmostEqual(
            result["result"]["price"],
            135.45,
            places=8,
        )


if __name__ == "__main__":
    unittest.main()
