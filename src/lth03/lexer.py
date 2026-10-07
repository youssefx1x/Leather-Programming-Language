from .tokens import Token


class LTH03LexError(Exception):
    pass


KEYWORDS = {
    "rule": "RULE",
    "when": "WHEN",
    "and": "AND",
    "or": "OR",
    "not": "NOT",
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL",
}


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.i = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def _advance(self):
        ch = self.source[self.i]
        self.i += 1

        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return ch

    def _peek(self, offset=0):
        index = self.i + offset

        if index >= len(self.source):
            return ""

        return self.source[index]

    def _string(self):
        line = self.line
        column = self.column

        self._advance()

        chars = []

        while self.i < len(self.source):
            ch = self._peek()

            if ch == '"':
                self._advance()
                return Token(
                    "STRING",
                    "".join(chars),
                    line,
                    column,
                )

            if ch == "\\":
                self._advance()

                if self.i >= len(self.source):
                    break

                escaped = self._advance()

                chars.append(
                    {
                        "n": "\n",
                        "t": "\t",
                        "r": "\r",
                        '"': '"',
                        "\\": "\\",
                    }.get(escaped, escaped)
                )

            else:
                chars.append(self._advance())

        raise LTH03LexError(
            f"unterminated string at {line}:{column}"
        )

    def _number(self):
        line = self.line
        column = self.column

        start = self.i
        dots = 0

        while self._peek().isdigit() or self._peek() == ".":
            if self._peek() == ".":
                dots += 1

            self._advance()

        raw = self.source[start:self.i]

        if dots > 1:
            raise LTH03LexError(
                f"invalid number {raw!r} at {line}:{column}"
            )

        value = float(raw) if "." in raw else int(raw)

        return Token(
            "NUMBER",
            value,
            line,
            column,
        )

    def _identifier(self):
        line = self.line
        column = self.column

        start = self.i
        self._advance()

        while (
            self._peek().isalnum()
            or self._peek() == "_"
        ):
            self._advance()

        raw = self.source[start:self.i]

        return Token(
            KEYWORDS.get(raw, "IDENT"),
            raw,
            line,
            column,
        )

    def tokenize(self):
        two_char = {
            "==": "EQ",
            "!=": "NE",
            "<=": "LE",
            ">=": "GE",
            "->": "ARROW",
            "+=": "PLUS_EQ",
            "-=": "MINUS_EQ",
            "*=": "STAR_EQ",
            "/=": "SLASH_EQ",
        }

        one_char = {
            "=": "ASSIGN",
            "<": "LT",
            ">": "GT",
            "+": "PLUS",
            "-": "MINUS",
            "*": "STAR",
            "/": "SLASH",
            "%": "PERCENT",
            "(": "LPAREN",
            ")": "RPAREN",
            "[": "LBRACKET",
            "]": "RBRACKET",
            "{": "LBRACE",
            "}": "RBRACE",
            ":": "COLON",
            ",": "COMMA",
            ";": "SEMI",
            ".": "DOT",
        }

        while self.i < len(self.source):
            ch = self._peek()

            if ch.isspace():
                self._advance()
                continue

            if ch == "#":
                while (
                    self.i < len(self.source)
                    and self._peek() != "\n"
                ):
                    self._advance()

                continue

            if ch == '"':
                self.tokens.append(self._string())
                continue

            if ch.isdigit():
                self.tokens.append(self._number())
                continue

            if ch.isalpha() or ch == "_":
                self.tokens.append(self._identifier())
                continue

            line = self.line
            column = self.column

            pair = self.source[self.i:self.i + 2]

            if pair in two_char:
                self._advance()
                self._advance()

                self.tokens.append(
                    Token(
                        two_char[pair],
                        pair,
                        line,
                        column,
                    )
                )

                continue

            if ch in one_char:
                self._advance()

                self.tokens.append(
                    Token(
                        one_char[ch],
                        ch,
                        line,
                        column,
                    )
                )

                continue

            raise LTH03LexError(
                f"unexpected character {ch!r} "
                f"at {line}:{column}"
            )

        self.tokens.append(
            Token(
                "EOF",
                "",
                self.line,
                self.column,
            )
        )

        return self.tokens
