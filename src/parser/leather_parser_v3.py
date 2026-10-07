from src.parser.leather_parser_v2 import LeatherParserV2
from src.parser.system import System


class LeatherParserV3(LeatherParserV2):
    def parse(self):
        statements = []

        while not self._check("EOF"):
            if self._check("RULE"):
                statements.append(self._rule())
            elif self._check("BASE"):
                statements.append(self._base())
            elif self._check("FLOW"):
                statements.append(self._flow())
            elif self._check("SYSTEM"):
                statements.append(self._system())
            else:
                statements.append(self._assignment_or_extension())

        from src.parser.parser import Program
        return Program(statements)

    def _system(self):
        self._consume(
            "SYSTEM",
            "expected 'system'"
        )

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
