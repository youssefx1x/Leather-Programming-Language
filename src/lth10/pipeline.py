from .contract import is_valid_source
from .discovery import discover
from .model import LeatherProgram


class LeatherPipeline:
    """
    LTH 1.0 canonical bootstrap pipeline.

    It reuses existing Leather components whenever they exist.
    It never creates a parallel semantic implementation.
    """

    VERSION = "1.0.0"

    def __init__(self):
        self.components = discover()

    def compile(self, source):
        if not isinstance(source, str):
            raise TypeError("Leather source must be a string")

        program = LeatherProgram(source=source)

        lexer_module = self.components.get("lexer")

        if lexer_module is not None:
            Lexer = getattr(lexer_module, "Lexer", None)

            if Lexer is not None:
                program.tokens = Lexer(source).tokenize()

        return program

    def status(self):
        return {
            name: module is not None
            for name, module in self.components.items()
        }
