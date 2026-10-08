import unittest

from src.lexer.lexer import Lexer


class TestLTH10LexerGrammar(unittest.TestCase):

    def test_arithmetic_tokens(self):
        tokens = Lexer(
            "a + b - c * d / e % f"
        ).tokenize()

        kinds = [token.kind for token in tokens]

        self.assertEqual(
            kinds,
            [
                "IDENTIFIER",
                "PLUS",
                "IDENTIFIER",
                "MINUS",
                "IDENTIFIER",
                "STAR",
                "IDENTIFIER",
                "SLASH",
                "IDENTIFIER",
                "PERCENT",
                "IDENTIFIER",
                "EOF",
            ],
        )

    def test_call_tokens(self):
        tokens = Lexer(
            "add(2, 3)"
        ).tokenize()

        kinds = [token.kind for token in tokens]

        self.assertEqual(
            kinds,
            [
                "IDENTIFIER",
                "LPAREN",
                "NUMBER",
                "COMMA",
                "NUMBER",
                "RPAREN",
                "EOF",
            ],
        )

    def test_block_tokens(self):
        tokens = Lexer(
            "rule add(a, b):"
        ).tokenize()

        kinds = [token.kind for token in tokens]

        self.assertEqual(
            kinds,
            [
                "RULE",
                "IDENTIFIER",
                "LPAREN",
                "IDENTIFIER",
                "COMMA",
                "IDENTIFIER",
                "RPAREN",
                "COLON",
                "EOF",
            ],
        )


if __name__ == "__main__":
    unittest.main()
