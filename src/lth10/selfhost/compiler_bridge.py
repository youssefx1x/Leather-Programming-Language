from pathlib import Path
import importlib


class LeatherCompilerBridge:
    """
    LTH 1.0 bridge into the canonical Leather compiler pipeline.

    The bridge discovers the existing lexer/parser implementation
    without replacing it or creating a second parser.
    """

    VERSION = "1.0"

    def _load_lexer(self):
        candidates = (
            "src.lexer.lexer",
            "src.lexer",
        )

        for name in candidates:
            try:
                module = importlib.import_module(name)

                if hasattr(module, "Lexer"):
                    return module.Lexer

            except ImportError:
                continue

        raise ImportError("Leather Lexer not found")

    def load_source(self, path):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        if path.suffix != ".lth":
            raise ValueError("Leather source must use .lth")

        return path.read_text()

    def tokenize(self, path):
        source = self.load_source(path)
        Lexer = self._load_lexer()

        lexer = Lexer(source)

        if hasattr(lexer, "tokenize"):
            return lexer.tokenize()

        if hasattr(lexer, "lex"):
            return lexer.lex()

        raise AttributeError(
            "Leather Lexer exposes neither tokenize() nor lex()"
        )

    def compiler_status(self):
        Lexer = self._load_lexer()

        return {
            "version": self.VERSION,
            "lexer": Lexer.__name__,
            "status": "AVAILABLE",
        }
