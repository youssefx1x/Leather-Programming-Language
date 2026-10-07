from src.sea_equivalence import (
    SEAEquivalenceRelation,
    quotient_values,
)


def main():
    values = (
        (1, 2),
        (2, 1),
        (1, 2),
        (3, 0),
        (0, 3),
    )

    relation = SEAEquivalenceRelation(
        lambda value: tuple(sorted(value))
    )

    result = relation.partition(values)

    assert result.original_count == 5
    assert result.class_count == 2
    assert result.reduction_ratio == 0.6
    assert len(quotient_values(
        values,
        lambda value: tuple(sorted(value)),
    )) == 2

    print("SEA 0.4 EQUIVALENCE/QUOTIENT: PASS")


if __name__ == "__main__":
    main()
