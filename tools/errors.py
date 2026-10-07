class LeatherError(Exception):
    """Base class for user-facing Leather errors."""

    error_type = "error"

    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def format(self):
        location = ""

        if self.line is not None:
            location = f" at {self.line}"

            if self.column is not None:
                location += f":{self.column}"

        return (
            f"LTH Error [{self.error_type}]{location}: "
            f"{self.message}"
        )


class LeatherLexError(LeatherError):
    error_type = "lexer"


class LeatherParseError(LeatherError):
    error_type = "parser"


class LeatherSemanticError(LeatherError):
    error_type = "semantic"


class LeatherIRError(LeatherError):
    error_type = "ir"


class LeatherRuntimeError(LeatherError):
    error_type = "runtime"


class LeatherInputError(LeatherError):
    error_type = "input"
