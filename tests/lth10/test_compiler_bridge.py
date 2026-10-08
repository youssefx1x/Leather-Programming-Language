import unittest
from pathlib import Path

from src.lth10.selfhost.compiler_bridge import LeatherCompilerBridge


class TestCompilerBridge(unittest.TestCase):

    def setUp(self):
        self.bridge = LeatherCompilerBridge()
        self.source = Path("src/lth10/selfhost/core.lth")

    def test_lexer_is_available(self):
        status = self.bridge.compiler_status()

        self.assertEqual(status["version"], "1.0")
        self.assertEqual(status["lexer"], "Lexer")
        self.assertEqual(status["status"], "AVAILABLE")

    def test_source_load(self):
        source = self.bridge.load_source(self.source)

        self.assertIn("value", source)
        self.assertIn("rule", source)
        self.assertIn("system", source)

    def test_tokenization(self):
        tokens = self.bridge.tokenize(self.source)

        self.assertIsNotNone(tokens)
        self.assertGreater(len(tokens), 0)


if __name__ == "__main__":
    unittest.main()
