import unittest
from pathlib import Path

from src.lth10.selfhost.bridge import LeatherSourceBridge


class TestSelfHostedBridge(unittest.TestCase):

    def test_core_source_loads(self):
        bridge = LeatherSourceBridge()

        source = bridge.load(
            Path("src/lth10/selfhost/core.lth")
        )

        self.assertTrue(source)

    def test_core_contains_language_constructs(self):
        bridge = LeatherSourceBridge()

        source = bridge.load(
            Path("src/lth10/selfhost/core.lth")
        )

        result = bridge.verify_core(source)

        self.assertTrue(all(result.values()))

    def test_core_is_valid(self):
        bridge = LeatherSourceBridge()

        source = bridge.load(
            Path("src/lth10/selfhost/core.lth")
        )

        self.assertTrue(bridge.is_valid_core(source))

    def test_wrong_extension(self):
        bridge = LeatherSourceBridge()

        with self.assertRaises(ValueError):
            bridge.load("README.md")


if __name__ == "__main__":
    unittest.main()
