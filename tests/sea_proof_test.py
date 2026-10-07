from src.sea_proof import (
    SEAComplexityClaim,
    SEAMeaningClaim,
    SEAProofStatus,
    SEAProofStep,
    certify,
)


def main():
    meaning = SEAMeaningClaim(
        source="naive-search",
        target="compressed-search",
        equivalent=True,
        basis="same reachable semantic states",
    )

    complexity = SEAComplexityClaim(
        source_cost=1000,
        target_cost=100,
        improved=True,
    )

    steps = (
        SEAProofStep(
            name="equivalence",
            statement=(
                "reachable semantic result "
                "is preserved"
            ),
            justified=True,
        ),
        SEAProofStep(
            name="reduction",
            statement=(
                "target cost is lower"
            ),
            justified=True,
        ),
    )

    certificate = certify(
        "state-compression",
        meaning,
        complexity,
        steps,
    )

    assert (
        certificate.status
        == SEAProofStatus.VALIDATED
    )

    assert (
        certificate.summary()[
            "complexity_improved"
        ]
        is True
    )

    rejected = certify(
        "unsafe",
        SEAMeaningClaim(
            source="a",
            target="b",
            equivalent=False,
            basis="none",
        ),
        complexity,
        steps,
    )

    assert (
        rejected.status
        == SEAProofStatus.REJECTED
    )

    print(
        "SEA 0.2 COMPLEXITY PROOF OBJECTS: PASS"
    )


if __name__ == "__main__":
    main()
