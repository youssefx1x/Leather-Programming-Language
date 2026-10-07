from dataclasses import dataclass


@dataclass(frozen=True)
class SEADomain:
    name: str
    initial: object
    expand: object
    goal: object
    key_fn: object = None
    metadata: tuple = ()

    def key(self, state):
        if self.key_fn is None:
            return state

        return self.key_fn(state)

    def describe(self):
        return {
            "name": self.name,
            "metadata": dict(self.metadata),
        }
