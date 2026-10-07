from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    kind: str
    value: object
    line: int
    column: int

    def __repr__(self):
        return (
            f"Token(kind={self.kind!r}, value={self.value!r}, "
            f"line={self.line}, column={self.column})"
        )
