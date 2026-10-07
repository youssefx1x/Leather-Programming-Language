from src.sea_compression import (
    SEACompression,
    certify_compression,
)


def main():
    transformation = SEACompression(
        original_states=1_000_000,
        compressed_states=1_000,
        semantics_preserved=True,
        method="structural_state_compression",
        evidence="equivalent state classes",
    )

    assert transformation.ratio == 1000
    assert transformation.reduced
    assert (
        transformation.percentage_reduction
        == 99.9
    )
    assert transformation.valid

    certificate = certify_compression(
        transformation
    )

    assert certificate.valid

    print(
        "SEA 0.2 COMPRESSION MODEL: PASS"
    )


if __name__ == "__main__":
    main()
