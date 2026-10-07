from .lexer import Lexer, LTH03LexError
from .parser import Parser, LTH03ParseError
from .runtime import (
    Evaluator,
    LTH03RuntimeError,
)


class LTH03Error(Exception):
    pass


class LTH03Runner:
    def run(self, source, context=None):
        try:
            tokens = Lexer(source).tokenize()
            program = Parser(tokens).parse()

            return Evaluator(
                context=context
            ).run(program)

        except (
            LTH03LexError,
            LTH03ParseError,
            LTH03RuntimeError,
        ) as error:
            raise LTH03Error(
                str(error)
            ) from error
