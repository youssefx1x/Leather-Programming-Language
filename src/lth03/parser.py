from .ast import (
    Assignment,
    Binary,
    Call,
    Index,
    ListLiteral,
    Literal,
    MapLiteral,
    Member,
    Name,
    Program,
    Rule,
    Unary,
)


class LTH03ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def current(self):
        return self.tokens[self.i]

    def at(self, kind):
        return self.current().kind == kind

    def take(self, kind=None):
        token = self.current()

        if kind is not None and token.kind != kind:
            raise LTH03ParseError(
                f"expected {kind}, got {token.kind} "
                f"at {token.line}:{token.column}"
            )

        self.i += 1
        return token

    def match(self, *kinds):
        if self.current().kind in kinds:
            return self.take()

        return None

    def parse(self):
        statements = []

        while not self.at("EOF"):
            if self.match("SEMI"):
                continue

            if self.at("RULE"):
                statements.append(self.rule())
            else:
                statements.append(self.assignment())

            self.match("SEMI")

        return Program(statements)

    def assignment(self):
        name = self.take("IDENT").value
        operator = self.take().kind

        operator_map = {
            "ASSIGN": "=",
            "PLUS_EQ": "+=",
            "MINUS_EQ": "-=",
            "STAR_EQ": "*=",
            "SLASH_EQ": "/=",
        }

        if operator not in operator_map:
            token = self.current()

            raise LTH03ParseError(
                "expected assignment operator "
                f"at {token.line}:{token.column}"
            )

        return Assignment(
            name=name,
            expr=self.expr(),
            op=operator_map[operator],
        )

    def rule(self):
        self.take("RULE")

        name = self.take("IDENT").value

        self.take("WHEN")

        condition = self.expr()

        self.take("ARROW")

        actions = [self.assignment()]

        while self.match("SEMI"):
            actions.append(self.assignment())

        return Rule(
            name=name,
            condition=condition,
            actions=actions,
        )

    def expr(self):
        return self.or_expr()

    def or_expr(self):
        node = self.and_expr()

        while self.match("OR"):
            node = Binary(
                node,
                "or",
                self.and_expr(),
            )

        return node

    def and_expr(self):
        node = self.equality()

        while self.match("AND"):
            node = Binary(
                node,
                "and",
                self.equality(),
            )

        return node

    def equality(self):
        node = self.compare()

        while self.at("EQ") or self.at("NE"):
            operator = self.take().value

            node = Binary(
                node,
                operator,
                self.compare(),
            )

        return node

    def compare(self):
        node = self.term()

        while (
            self.at("LT")
            or self.at("LE")
            or self.at("GT")
            or self.at("GE")
        ):
            operator = self.take().value

            node = Binary(
                node,
                operator,
                self.term(),
            )

        return node

    def term(self):
        node = self.factor()

        while (
            self.at("PLUS")
            or self.at("MINUS")
        ):
            operator = self.take().value

            node = Binary(
                node,
                operator,
                self.factor(),
            )

        return node

    def factor(self):
        node = self.unary()

        while (
            self.at("STAR")
            or self.at("SLASH")
            or self.at("PERCENT")
        ):
            operator = self.take().value

            node = Binary(
                node,
                operator,
                self.unary(),
            )

        return node

    def unary(self):
        if self.at("NOT") or self.at("MINUS"):
            operator = self.take().value

            return Unary(
                operator,
                self.unary(),
            )

        return self.postfix()

    def postfix(self):
        node = self.primary()

        while True:
            if self.match("DOT"):
                node = Member(
                    node,
                    self.take("IDENT").value,
                )

            elif self.match("LBRACKET"):
                index = self.expr()

                self.take("RBRACKET")

                node = Index(
                    node,
                    index,
                )

            elif (
                isinstance(node, Name)
                and self.match("LPAREN")
            ):
                args = []

                if not self.at("RPAREN"):
                    args.append(self.expr())

                    while self.match("COMMA"):
                        args.append(self.expr())

                self.take("RPAREN")

                node = Call(
                    node.name,
                    args,
                )

            else:
                break

        return node

    def primary(self):
        token = self.current()

        if token.kind == "NUMBER":
            self.take()
            return Literal(token.value)

        if token.kind == "STRING":
            self.take()
            return Literal(token.value)

        if token.kind == "TRUE":
            self.take()
            return Literal(True)

        if token.kind == "FALSE":
            self.take()
            return Literal(False)

        if token.kind == "NULL":
            self.take()
            return Literal(None)

        if token.kind == "IDENT":
            self.take()
            return Name(token.value)

        if self.match("LPAREN"):
            node = self.expr()

            self.take("RPAREN")

            return node

        if self.match("LBRACKET"):
            items = []

            if not self.at("RBRACKET"):
                items.append(self.expr())

                while self.match("COMMA"):
                    items.append(self.expr())

            self.take("RBRACKET")

            return ListLiteral(items)

        if self.match("LBRACE"):
            items = []

            if not self.at("RBRACE"):
                key = self.take("IDENT").value

                self.take("COLON")

                items.append(
                    (key, self.expr())
                )

                while self.match("COMMA"):
                    key = self.take("IDENT").value

                    self.take("COLON")

                    items.append(
                        (key, self.expr())
                    )

            self.take("RBRACE")

            return MapLiteral(items)

        raise LTH03ParseError(
            f"unexpected {token.kind} "
            f"at {token.line}:{token.column}"
        )
