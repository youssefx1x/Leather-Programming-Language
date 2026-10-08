import unittest

from src.lth05.runner import LTH05Runner


class LTH05LanguageTest(unittest.TestCase):
    def test_assignment_and_expression(self):
        source = """
price = 150.5
total = price * 2
"""

        result = LTH05Runner().run(source)

        self.assertEqual(result.values["price"], 150.5)
        self.assertEqual(result.values["total"], 301.0)

    def test_rule_execution(self):
        source = """
price = 150.5
rule discount when customer.vip -> price *= 0.9
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

    def test_list_and_call(self):
        source = """
items = [1, 2, 3]
count = len(items)
"""

        result = LTH05Runner().run(source)

        self.assertEqual(result.values["items"], [1, 2, 3])
        self.assertEqual(result.values["count"], 3)


if __name__ == "__main__":
    unittest.main()
