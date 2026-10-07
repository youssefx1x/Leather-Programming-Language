from dataclasses import dataclass


@dataclass(frozen=True)
class SEAEquivalenceClass:
    key: object
    members: tuple

    @property
    def size(self):
        return len(self.members)


@dataclass(frozen=True)
class SEAEquivalenceResult:
    original_count: int
    class_count: int
    compression_ratio: float
    classes: tuple

    @property
    def reduced_count(self):
        return self.class_count

    @property
    def reduction_ratio(self):
        if self.original_count == 0:
            return 0.0

        return 1.0 - (
            self.class_count / self.original_count
        )


class SEAEquivalenceRelation:
    """
    Explicit semantic equivalence relation.

    Two states are equivalent when key_fn(state) is equal.
    """

    def __init__(self, key_fn):
        self.key_fn = key_fn

    def key(self, value):
        return self.key_fn(value)

    def equivalent(self, left, right):
        return self.key(left) == self.key(right)

    def partition(self, values):
        buckets = {}

        for value in values:
            key = self.key(value)
            buckets.setdefault(key, []).append(value)

        classes = tuple(
            SEAEquivalenceClass(
                key=key,
                members=tuple(members),
            )
            for key, members in buckets.items()
        )

        original_count = len(values)
        class_count = len(classes)

        compression_ratio = (
            original_count / class_count
            if class_count
            else 1.0
        )

        return SEAEquivalenceResult(
            original_count=original_count,
            class_count=class_count,
            compression_ratio=compression_ratio,
            classes=classes,
        )


def quotient_values(values, key_fn):
    relation = SEAEquivalenceRelation(key_fn)
    result = relation.partition(values)

    return tuple(
        cls.members[0]
        for cls in result.classes
    )
