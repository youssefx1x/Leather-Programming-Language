from dataclasses import dataclass


class FlowError(Exception):
    pass


@dataclass(frozen=True)
class FlowDefinition:
    name: str
    source: str


class FlowRegistry:
    def __init__(self):
        self._flows = {}

    def define(self, name, source):
        if name in self._flows:
            raise FlowError(
                f"flow '{name}' already exists"
            )

        self._flows[name] = FlowDefinition(
            name=name,
            source=source.strip(),
        )

        return self._flows[name]

    def get(self, name):
        if name not in self._flows:
            raise FlowError(
                f"unknown flow '{name}'"
            )
        return self._flows[name]

    def names(self):
        return tuple(self._flows)

    def expand(self, name, stack=None):
        stack = tuple(stack or ())

        if name in stack:
            chain = " -> ".join(
                (*stack, name)
            )
            raise FlowError(
                f"flow composition cycle: {chain}"
            )

        return self.get(name).source

    def items(self):
        return tuple(self._flows.items())
