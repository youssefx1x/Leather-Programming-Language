from src.sea_space_algebra import (
    SEAAlternativeSpace,
    SEACompressedStateClasses,
    SEAStateSpaceAlgebra,
)


def main():
    a = SEAStateSpaceAlgebra(
        dimensions=(10, 20)
    )

    b = SEAStateSpaceAlgebra(
        dimensions=(30, 40)
    )

    assert a.total_states() == 200
    assert b.total_states() == 1200

    product = a.product(b)

    assert product.total_states() == 240000

    alternatives = a.add_alternatives(b)

    assert isinstance(
        alternatives,
        SEAAlternativeSpace,
    )

    assert alternatives.total_states() == 1400

    compressed = SEACompressedStateClasses(
        raw_states=1_000_000,
        equivalence_classes=10_000,
    )

    assert compressed.ratio == 100
    assert compressed.reduction == 0.99
    assert compressed.valid_compression

    print(
        "SEA 0.3 STATE-SPACE ALGEBRA: PASS"
    )


if __name__ == "__main__":
    main()
