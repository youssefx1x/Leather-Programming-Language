from src.runtime.morphic import MorphicValue


class MorphicRegistry:
    def __init__(self):
        self.values = {}

    def define(
        self,
        name,
        semantic_type,
        value,
        representation="native",
    ):
        morphic = MorphicValue(
            name=name,
            semantic_type=semantic_type,
            value=value,
            representation=representation,
        )

        self.values[name] = morphic
        return morphic

    def get(self, name):
        return self.values.get(name)

    def morph(self, name, representation, value=None):
        morphic = self.get(name)

        if morphic is None:
            raise KeyError(
                f"unknown morphic value '{name}'"
            )

        return morphic.morph(
            representation,
            value,
        )

    def describe(self):
        lines = ["MORPHIC REGISTRY"]

        for morphic in self.values.values():
            lines.append(
                f"  {morphic.describe()}"
            )

        return "\n".join(lines)
