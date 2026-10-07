from dataclasses import dataclass


@dataclass
class MorphicValue:
    """
    A value whose semantic identity remains stable while
    its runtime representation may change.
    """

    name: str
    semantic_type: str
    value: object
    representation: str = "native"

    def morph(self, representation, value=None):
        self.representation = representation

        if value is not None:
            self.value = value

        return self

    def describe(self):
        return (
            f"MORPHIC {self.name} "
            f"type={self.semantic_type} "
            f"representation={self.representation} "
            f"value={self.value}"
        )
