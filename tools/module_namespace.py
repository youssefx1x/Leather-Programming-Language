from dataclasses import dataclass, field


class ModuleNamespaceError(Exception):
    pass


@dataclass
class ModuleNamespace:
    name: str
    symbols: dict = field(default_factory=dict)

    def define(self, name, value):
        if name in self.symbols:
            raise ModuleNamespaceError(
                f"duplicate symbol '{name}' "
                f"in module '{self.name}'"
            )

        self.symbols[name] = value

    def get(self, name):
        if name not in self.symbols:
            raise ModuleNamespaceError(
                f"unknown symbol '{name}' "
                f"in module '{self.name}'"
            )

        return self.symbols[name]


class NamespaceRegistry:
    def __init__(self):
        self.modules = {}

    def create(self, name):
        if name in self.modules:
            raise ModuleNamespaceError(
                f"module namespace '{name}' "
                f"already exists"
            )

        namespace = ModuleNamespace(name)
        self.modules[name] = namespace
        return namespace

    def get(self, name):
        if name not in self.modules:
            raise ModuleNamespaceError(
                f"unknown module '{name}'"
            )

        return self.modules[name]
