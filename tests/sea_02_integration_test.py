from src.sea_complexity import (
    SEAComplexity,
    ComplexityExpr,
)
from src.sea_compression import (
    SEACompression,
    certify_compression,
)
from src.sea_growth import (
    classify_growth,
    symbolic_growth_relation,
)
from src.sea_laws import SEAComplexityLawSet
from src.sea_proof import (
    SEAComplexityClaim,
    SEAMeaningClaim,
    SEAProofStep,
    SEAProofStatus,
    certify,
)


def main():
    n = ComplexityExpr.symbol("n")

    raw = n ** 2
    search = 2 ** n

    assert classify_growth(
        raw
    ) == "quadratic"

    assert classify_growth(
        search
    ) == "exponential"

    assert (
        symbolic_growth_relation(
            raw,
            search,
        ).relation
        == "slower_growth"
    )

    first = SEAComplexity(
        time=n ** 2,
        memory=n,
        states=2 ** n,
        branching=2,
        depth=n,
        precision=1,
        interactions=n,
    )

    second = SEAComplexity(
        time=n,
        memory=n,
        states=n ** 2,
        branching=2,
        depth=n,
        precision=1,
        interactions=n,
    )

    laws = SEAComplexityLawSet()

    combined = laws.sequential(
        first,
        second,
    )

    assert (
        combined.time.evaluate(
            {"n": 10}
        )
        == 110
    )

    compression = SEACompression(
        original_states=1_000_000,
        compressed_states=1_000,
        semantics_preserved=True,
        method="equivalence-class-compression",
    )

    compression_certificate = (
        certify_compression(
            compression
        )
    )

    assert compression_certificate.valid

    certificate = certify(
        "integrated-sea-optimization",
        SEAMeaningClaim(
            source="raw-state-space",
            target="compressed-state-space",
            equivalent=True,
            basis="validated equivalence classes",
        ),
        SEAComplexityClaim(
            source_cost=1_000_000,
            target_cost=1_000,
            improved=True,
        ),
        (
            SEAProofStep(
                "semantic-equivalence",
                "meaning preserved",
                True,
            ),
            SEAProofStep(
                "complexity-reduction",
                "state count reduced",
                True,
            ),
        ),
    )

    assert (
        certificate.status
        == SEAProofStatus.VALIDATED
    )

    print(
        "SEA 0.2 INTEGRATION: PASS"
    )


if __name__ == "__main__":
    main()
