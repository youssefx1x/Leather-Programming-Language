from dataclasses import dataclass
from pathlib import Path
import importlib.util
import time


class LTHError(Exception):
    """Base Leather-native error."""


class LTHModuleError(LTHError):
    """Module loading/import error."""


class LTHExecutionError(LTHError):
    """Execution error."""


@dataclass
class ExecutionReport:
    source: str
    elapsed_ns: int
    success: bool
    output: str = ""

    @property
    def elapsed_ms(self):
        return self.elapsed_ns / 1_000_000


class ModuleLoader:
    """Small stable module loader for the 0.9.1 application layer."""

    def load(self, path):
        path = Path(path)

        if not path.exists():
            raise LTHModuleError(f"module not found: {path}")

        if path.suffix != ".py":
            raise LTHModuleError(
                f"unsupported module type: {path.suffix}"
            )

        name = f"lth_module_{path.stem}"

        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise LTHModuleError(f"cannot load module: {path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


class LTHRuntime:
    """
    Stable application/runtime facade.

    The underlying LTH 0.1 semantics remain authoritative.
    This layer adds stable application behavior around them.
    """

    VERSION = "0.9.1"

    def __init__(self):
        self.modules = ModuleLoader()

    def execute(self, source, action=None):
        start = time.perf_counter_ns()

        try:
            if action is None:
                output = source
            else:
                output = action(source)

            elapsed = time.perf_counter_ns() - start

            return ExecutionReport(
                source=str(source),
                elapsed_ns=elapsed,
                success=True,
                output=str(output),
            )

        except LTHError:
            raise

        except Exception as exc:
            raise LTHExecutionError(str(exc)) from exc
