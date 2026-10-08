from pathlib import Path

from .runtime import LTHRuntime, LTHExecutionError


class LeatherRunner:
    """
    Official 0.9.1 runner facade.

    It deliberately keeps the stable runtime boundary small so the
    existing 0.1 implementation remains compatible.
    """

    VERSION = "0.9.1"

    def __init__(self):
        self.runtime = LTHRuntime()

    def run_text(self, text):
        if not isinstance(text, str):
            raise LTHExecutionError("source must be a string")

        return self.runtime.execute(text)

    def run_file(self, path):
        path = Path(path)

        if not path.exists():
            raise LTHExecutionError(f"source file not found: {path}")

        try:
            source = path.read_text()
        except OSError as exc:
            raise LTHExecutionError(str(exc)) from exc

        return self.run_text(source)

    def version(self):
        return self.VERSION
