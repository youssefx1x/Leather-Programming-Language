from src.sea_complexity import SEAComplexity
from src.sea_transform import (
    SEAOptimizationCertificate,
    SEATransformation,
)


def main():
    source = SEAComplexity(
        time=100,
        memory=50,
        states=1000,
        branching=8,
        depth=20,
        precision=4,
        interactions=40,
    )

    target = SEAComplexity(
        time=20,
        memory=40,
        states=500,
        branching=4,
        depth=10,
        precision=4,
        interactions=20,
    )

    transformation = SEATransformation(
        source="naive",
        target="compressed",
        name="state_compression",
        semantics_preserved=True,
        rationale="preserve meaning while reducing redundant states",
    )

    assert transformation.semantics_preserved

    certificate = SEAOptimizationCertificate(
        source_complexity=source,
        target_complexity=target,
        semantics_preserved=True,
        transformation_name=(
            transformation.name
        ),
    )

    assert certificate.complexity_improved
    assert certificate.valid

    summary = certificate.summary()

    assert summary["valid"] is True

    invalid = SEAOptimizationCertificate(
        source_complexity=source,
        target_complexity=target,
        semantics_preserved=False,
        transformation_name="unsafe_change",
    )

    assert invalid.complexity_improved
    assert invalid.valid is False

    print("SEA 0.1 OPTIMIZATION SEMANTICS: PASS")


if __name__ == "__main__":
    main()
