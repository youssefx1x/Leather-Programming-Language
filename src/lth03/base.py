from copy import deepcopy
from dataclasses import dataclass, field


class BaseError(Exception):
    pass


@dataclass
class BaseDefinition:
    name: str
    fields: dict = field(default_factory=dict)
    extends: str | None = None

    def define(self, name, value):
        if name in self.fields:
            raise BaseError(
                f"duplicate field '{name}' in base '{self.name}'"
            )
        self.fields[name] = value

    def instantiate(self, overrides=None):
        values = deepcopy(self.fields)

        if overrides is not None:
            if not isinstance(overrides, dict):
                raise BaseError(
                    f"base '{self.name}' overrides must be a map"
                )

            unknown = sorted(
                set(overrides) - set(values)
            )

            if unknown:
                raise BaseError(
                    f"unknown override field(s) for base "
                    f"'{self.name}': {', '.join(unknown)}"
                )

            values.update(deepcopy(overrides))

        return BaseInstance(self.name, values)


class BaseInstance(dict):
    def __init__(self, base_name, values):
        super().__init__(deepcopy(values))
        self._base_name = base_name

    @property
    def base_name(self):
        return self._base_name

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(name) from error

    def __repr__(self):
        return f"<{self._base_name} {dict.__repr__(self)}>"


class BaseRegistry:
    def __init__(self):
        self._bases = {}

    def define(self, name, fields=None, extends=None):
        if name in self._bases:
            raise BaseError(f"base '{name}' already exists")

        if extends == name:
            raise BaseError(
                f"base '{name}' cannot extend itself"
            )

        base = BaseDefinition(
            name=name,
            fields=dict(fields or {}),
            extends=extends,
        )

        self._bases[name] = base
        return base

    def get(self, name):
        if name not in self._bases:
            raise BaseError(f"unknown base '{name}'")
        return self._bases[name]

    def _resolve_fields(self, name, stack=None):
        stack = list(stack or [])

        if name in stack:
            chain = " -> ".join(stack + [name])
            raise BaseError(
                f"base inheritance cycle: {chain}"
            )

        base = self.get(name)

        if base.extends:
            parent_values = self._resolve_fields(
                base.extends,
                stack + [name],
            )
        else:
            parent_values = {}

        parent_values.update(
            deepcopy(base.fields)
        )

        return parent_values

    def validate(self):
        for name in self._bases:
            self._resolve_fields(name)

        return True

    def instantiate(self, name, overrides=None):
        values = self._resolve_fields(name)

        if overrides is not None:
            if not isinstance(overrides, dict):
                raise BaseError(
                    f"base '{name}' overrides must be a map"
                )

            unknown = sorted(
                set(overrides) - set(values)
            )

            if unknown:
                raise BaseError(
                    f"unknown override field(s) for base "
                    f"'{name}': {', '.join(unknown)}"
                )

            values.update(deepcopy(overrides))

        return BaseInstance(name, values)

    def names(self):
        return tuple(self._bases)
