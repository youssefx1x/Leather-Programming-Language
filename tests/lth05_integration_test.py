import unittest

from src.lth05.runner import LTH05Runner


class LTH05IntegrationTest(unittest.TestCase):
    def test_end_to_end(self):
        source = """
price = 150.5
rule discount when customer.vip -> price *= 0.9
items = [1, 2, 3]
count = len(items)
total = price * count
"""

        result = LTH05Runner().run(
            source,
            context={
                "customer": {
                    "vip": True,
                }
            },
        )

        self.assertAlmostEqual(
            result.values["price"],
            135.45,
            places=8,
        )
        self.assertEqual(
            result.values["count"],
            3,
        )
        self.assertAlmostEqual(
            result.values["total"],
            406.35,
            places=8,
        )

        meta = result.values["_lth05"]

        self.assertIn(
            "optimization",
            meta,
        )
        self.assertIn(
            "profile",
            meta,
        )


if __name__ == "__main__":
    unittest.main()
