import unittest

from src.lth10.contract import (
    REQUIRED_CONCEPTS,
    is_valid_source,
    verify_source_shape,
)
from src.lth10.discovery import discover
from src.lth10.pipeline import LeatherPipeline


class TestLTH10Release(unittest.TestCase):

    def test_identity(self):
        from src.lth10 import __version__
        self.assertEqual(__version__, "1.0.0")

    def test_source_shape(self):
        source = open(
            "src/lth10/selfhost/core.lth",
            encoding="utf-8",
        ).read()

        result = verify_source_shape(source)

        self.assertEqual(
            set(result),
            set(REQUIRED_CONCEPTS),
        )
        self.assertTrue(is_valid_source(source))

    def test_pipeline_exists(self):
        pipeline = LeatherPipeline()

        self.assertEqual(
            pipeline.VERSION,
            "1.0.0",
        )

    def test_lexer_integration(self):
        pipeline = LeatherPipeline()
        source = open(
            "src/lth10/selfhost/core.lth",
            encoding="utf-8",
        ).read()

        program = pipeline.compile(source)

        self.assertIsNotNone(program.tokens)
        self.assertGreater(len(program.tokens), 0)

    def test_component_discovery(self):
        components = discover()

        self.assertIn("lexer", components)
        self.assertIn("parser", components)
        self.assertIn("runtime", components)

        self.assertIsNotNone(components["lexer"])

    def test_pipeline_status(self):
        status = LeatherPipeline().status()

        self.assertTrue(status["lexer"])


if __name__ == "__main__":
    unittest.main()
