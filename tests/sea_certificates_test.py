from src.sea_certificates import (
    SEACondition,
    certify_optimization,
)


def main():
    certificate = certify_optimization(
        name="test",
        source_result=55,
        target_result=55,
        semantic_equivalence=True,
        conditions=(
            SEACondition(
                "same_output",
                True,
            ),
            SEACondition(
                "valid_measurement",
                True,
            ),
        ),
    )

    assert certificate.valid
    assert certificate.conditions_valid
    assert certificate.summary()["valid"]

    print("SEA 1.0 CERTIFICATES: PASS")


if __name__ == "__main__":
    main()
