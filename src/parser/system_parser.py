from src.parser.parser import Parser
from src.parser.system import System


class SystemParser(Parser):
    def parse(self):
        statements = []

        while not self._check("EOF"):
            if self._check("SYSTEM"):
                statements.append(self._system())
            else:
                raise self._unexpected_statement()

        from src.parser.parser import Program
        return Program(statements)

    def _system(self):
        self._consume("SYSTEM", "expected 'system'")

        name = self._consume(
            "IDENTIFIER",
            "expected system name"
        )

        self._consume(
            "ASSIGN",
            "expected '='"
        )

        components = []

        first = self._consume(
            "IDENTIFIER",
            "expected system component"
        )

        components.append(first.value)

        while self._check("ARROW"):
            self._advance()

            component = self._consume(
                "IDENTIFIER",
                "expected system component after '->'"
            )

            components.append(component.value)

        return System(
            name=name.value,
            components=components,
        )

    def _unexpected_statement(self):
        from src.parser.parser import ParserError

        token = self._current()

        return ParserError(
            f"unexpected token {token.kind} "
            f"at {token.line}:{token.column}"
        )
