from dataclasses import dataclass
from pathlib import Path


class ModuleLoadError(Exception):
    pass


@dataclass(frozen=True)
class LTHModule:
    path: Path
    source: str


class ModuleLoader:
    def __init__(self):
        self.loaded = {}

    def load(self, path):
        path = Path(path).resolve()

        if not path.exists():
            raise ModuleLoadError(
                f"module not found: {path}"
            )

        if not path.is_file():
            raise ModuleLoadError(
                f"module path is not a file: {path}"
            )

        if path.suffix != ".lth":
            raise ModuleLoadError(
                f"unsupported module type: {path.suffix}"
            )

        key = str(path)

        if key in self.loaded:
            return self.loaded[key]

        try:
            source = path.read_text(
                encoding="utf-8"
            )
        except OSError as error:
            raise ModuleLoadError(
                f"cannot read module: {error}"
            ) from error

        module = LTHModule(
            path=path,
            source=source,
        )

        self.loaded[key] = module

        return module

    def load_many(self, paths):
        return [
            self.load(path)
            for path in paths
        ]
