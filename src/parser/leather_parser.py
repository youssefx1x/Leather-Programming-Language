from src.parser.parser import Parser
from src.parser.base_flow import (
    Base,
    BaseExtension,
    Flow,
)


class LeatherParser(Parser):
    def parse(self):
        statements = []

        while not self._check("EOF"):
            if self._check("RULE"):
                statements.append(self._rule())

            elif self._check("BASE"):
                statements.append(self._base())

            elif self._check("FLOW"):
                statements.append(self._flow())

            else:
                statements.append(self._assignment_or_extension())

        from src.parser.parser import Program

        return Program(statements)

    def _base(self):
        self._consume(
            "BASE",
            "expected 'base'",
        )

        name = self._consume(
            "IDENTIFIER",
            "expected base name",
        )

        self._consume(
            "ASSIGN",
            "expected '='",
        )

        service = self._consume(
            "IDENTIFIER",
            "expected base service",
        )

        options = []

        while self._check("IDENTIFIER"):
            key = self._advance().value

            self._consume(
                "ASSIGN",
                "expected '=' after base option",
            )

            value = self._value()

            options.append(
                (key, value)
            )

        return Base(
            name=name.value,
            service=service.value,
            options=options,
        )

    def _assignment_or_extension(self):
        name = self._consume(
            "IDENTIFIER",
            "expected identifier",
        )

        self._consume(
            "ASSIGN",
            "expected '='",
        )

        if self._check("IDENTIFIER"):
            base_name = self._advance().value

            if self._check("WITH"):
                self._advance()

                options = []

                while self._check("IDENTIFIER"):
                    key = self._advance().value

                    self._consume(
                        "ASSIGN",
                        "expected '=' after extension option",
                    )

                    value = self._value()

                    options.append(
                        (key, value)
                    )

                return BaseExtension(
                    name=name.value,
                    base_name=base_name,
                    options=options,
                )

            raise self._extension_error()

        return self._assignment_after_name(name)

    def _assignment_after_name(self, name):
        value = self._value()

        from src.parser.parser import Assignment

        return Assignment(
            name=name.value,
            value=value,
        )

    def _extension_error(self):
        token = self._current()

        from src.parser.parser import ParserError

        raise ParserError(
            f"unexpected token after base name "
            f"at {token.line}:{token.column}"
        )

    def _flow(self):
        self._consume(
            "FLOW",
            "expected 'flow'",
        )

        name = self._consume(
            "IDENTIFIER",
            "expected flow name",
        )

        self._consume(
            "ASSIGN",
            "expected '='",
        )

        steps = []

        first = self._consume(
            "IDENTIFIER",
            "expected flow step",
        )

        steps.append(first.value)

        while self._check("ARROW"):
            self._advance()

            step = self._consume(
                "IDENTIFIER",
                "expected flow step after '->'",
            )

            steps.append(step.value)

        return Flow(
            name=name.value,
            steps=steps,
        )
