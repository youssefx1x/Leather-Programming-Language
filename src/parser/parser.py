from dataclasses import dataclass


@dataclass
class Program:
    statements: list


@dataclass
class Assignment:
    name: str
    value: object


@dataclass
class StringValue:
    value: str


@dataclass
class NumberValue:
    value: str


@dataclass
class MemberAccess:
    object_name: str
    member_name: str


@dataclass
class Rule:
    name: str
    condition: MemberAccess
    action_target: str
    action_operator: str
    action_value: object


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []

        while not self._check("EOF"):
            if self._check("RULE"):
                statements.append(self._rule())
            else:
                statements.append(self._assignment())

        return Program(statements)

    def _assignment(self):
        name = self._consume(
            "IDENTIFIER",
            "expected identifier",
        )

        self._consume(
            "ASSIGN",
            "expected '='",
        )

        value = self._value()

        return Assignment(
            name=name.value,
            value=value,
        )

    def _rule(self):
        self._consume(
            "RULE",
            "expected 'rule'",
        )

        name = self._consume(
            "IDENTIFIER",
            "expected rule name",
        )

        self._consume(
            "WHEN",
            "expected 'when'",
        )

        condition = self._member_access()

        self._consume(
            "ARROW",
            "expected '->'",
        )

        action_target = self._consume(
            "IDENTIFIER",
            "expected action target",
        )

        action_operator = self._consume(
            "STAR_EQUAL",
            "expected '*='",
        )

        action_value = self._value()

        return Rule(
            name=name.value,
            condition=condition,
            action_target=action_target.value,
            action_operator=action_operator.value,
            action_value=action_value,
        )

    def _member_access(self):
        object_name = self._consume(
            "IDENTIFIER",
            "expected object name",
        )

        self._consume(
            "DOT",
            "expected '.'",
        )

        member_name = self._consume(
            "IDENTIFIER",
            "expected member name",
        )

        return MemberAccess(
            object_name=object_name.value,
            member_name=member_name.value,
        )

    def _value(self):
        if self._check("STRING"):
            token = self._advance()
            return StringValue(token.value)

        if self._check("NUMBER"):
            token = self._advance()
            return NumberValue(token.value)

        token = self._current()

        raise ParserError(
            f"unexpected token {token.kind} at "
            f"{token.line}:{token.column}"
        )

    def _consume(self, kind, message):
        if self._check(kind):
            return self._advance()

        token = self._current()

        raise ParserError(
            f"{message} at "
            f"{token.line}:{token.column}"
        )

    def _check(self, kind):
        return self._current().kind == kind

    def _advance(self):
        token = self._current()

        if token.kind != "EOF":
            self.position += 1

        return token

    def _current(self):
        return self.tokens[self.position]
