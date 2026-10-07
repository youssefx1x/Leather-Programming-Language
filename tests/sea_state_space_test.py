from src.sea_state_space import (
    SEAStateSpace,
    SEACompressedSpace,
)


def main():
    space = SEAStateSpace(
        dimensions=(10, 20, 30)
    )

    assert space.dimension_count == 3
    assert space.state_count() == 6000

    huge = SEAStateSpace(
        dimensions=(
            10 ** 10,
            10 ** 20,
            10 ** 30,
        )
    )

    count = huge.huge_state_count()

    assert count.scientific_exponent == 60

    entropy = huge.entropy_like_measure()

    assert entropy > 190

    compressed = SEACompressedSpace(
        original=huge,
        compression_factor=10 ** 10,
    )

    compressed_count = (
        compressed.compressed_state_count()
    )

    assert (
        compressed_count.log10()
        < count.log10()
    )

    assert compressed.reduction_ratio() == 10 ** 10

    print("SEA 0.1 STATE SPACE MODEL: PASS")


if __name__ == "__main__":
    main()
