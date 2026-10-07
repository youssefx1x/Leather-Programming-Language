from dataclasses import dataclass


KEYWORDS = {
    "rule",
    "base",
    "flow",
    "system",
    "when",
    "with",
}


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int


class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LTH Lexer Error at {line}:{column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self):
        tokens = []

        while not self._at_end():
            char = self._current()

            if char in " \t\r":
                self._advance()
                continue

            if char == "\n":
                self._advance()
                self.line += 1
                self.column = 1
                continue

            if char == "#":
                self._skip_comment()
                continue

            if char.isalpha() or char == "_":
                tokens.append(self._identifier())
                continue

            if char.isdigit():
                tokens.append(self._number())
                continue

            if char == '"':
                tokens.append(self._string())
                continue

            line = self.line
            column = self.column

            if char == "=":
                self._advance()
                if self._current() == "=":
                    self._advance()
                    tokens.append(Token("EQUAL_EQUAL", "==", line, column))
                else:
                    tokens.append(Token("ASSIGN", "=", line, column))
                continue

            if char == "*":
                self._advance()
                if self._current() == "=":
                    self._advance()
                    tokens.append(Token("STAR_EQUAL", "*=", line, column))
                else:
                    tokens.append(Token("STAR", "*", line, column))
                continue

            if char == "-":
                self._advance()
                if self._current() == ">":
                    self._advance()
                    tokens.append(Token("ARROW", "->", line, column))
                else:
                    tokens.append(Token("MINUS", "-", line, column))
                continue

            if char == ".":
                self._advance()
                tokens.append(Token("DOT", ".", line, column))
                continue

            raise LexerError(
                f"unexpected character {char!r}",
                line,
                column,
            )

        tokens.append(Token("EOF", "", self.line, self.column))
        return tokens

    def _identifier(self):
        line = self.line
        column = self.column
        start = self.position

        while not self._at_end():
            char = self._current()

            if char.isalnum() or char == "_":
                self._advance()
            else:
                break

        value = self.source[start:self.position]

        if value in KEYWORDS:
            kind = value.upper()
        else:
            kind = "IDENTIFIER"

        return Token(kind, value, line, column)

    def _number(self):
        line = self.line
        column = self.column
        start = self.position

        while not self._at_end() and self._current().isdigit():
            self._advance()

        if not self._at_end() and self._current() == ".":
            self._advance()

            if self._at_end() or not self._current().isdigit():
                raise LexerError(
                    "expected digits after decimal point",
                    self.line,
                    self.column,
                )

            while not self._at_end() and self._current().isdigit():
                self._advance()

        value = self.source[start:self.position]
        return Token("NUMBER", value, line, column)

    def _string(self):
        line = self.line
        column = self.column

        self._advance()
        characters = []

        while not self._at_end():
            char = self._current()

            if char == '"':
                self._advance()
                return Token(
                    "STRING",
                    "".join(characters),
                    line,
                    column,
                )

            if char == "\\":
                self._advance()

                if self._at_end():
                    raise LexerError(
                        "unterminated escape sequence",
                        self.line,
                        self.column,
                    )

                escaped = self._current()
                self._advance()

                escapes = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    '"': '"',
                    "\\": "\\",
                }

                characters.append(escapes.get(escaped, escaped))
                continue

            if char == "\n":
                raise LexerError(
                    "unterminated string",
                    self.line,
                    self.column,
                )

            characters.append(char)
            self._advance()

        raise LexerError(
            "unterminated string",
            line,
            column,
        )

    def _skip_comment(self):
        while not self._at_end() and self._current() != "\n":
            self._advance()

    def _current(self):
        if self._at_end():
            return "\0"
        return self.source[self.position]

    def _advance(self):
        if self._at_end():
            return "\0"

        char = self.source[self.position]
        self.position += 1
        self.column += 1
        return char

    def _at_end(self):
        return self.position >= len(self.source)
