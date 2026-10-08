from dataclasses import dataclass


class SystemError(Exception):
    pass


@dataclass(frozen=True)
class SystemDefinition:
    name: str
    flows: tuple


class SystemRegistry:
    def __init__(self):
        self._systems = {}

    def define(self, name, flows):
        if name in self._systems:
            raise SystemError(
                f"system '{name}' already exists"
            )

        normalized = tuple(flows)

        if not normalized:
            raise SystemError(
                f"system '{name}' must use at least one flow"
            )

        self._systems[name] = SystemDefinition(
            name=name,
            flows=normalized,
        )

        return self._systems[name]

    def get(self, name):
        if name not in self._systems:
            raise SystemError(
                f"unknown system '{name}'"
            )
        return self._systems[name]

    def names(self):
        return tuple(self._systems)

    def items(self):
        return tuple(self._systems.items())

    def expand(self, name, flow_registry):
        system = self.get(name)

        return "\n".join(
            flow_registry.expand(flow_name)
            for flow_name in system.flows
        )
