from src.leather_performance import (
    LeatherPerformanceEngine,
)
from src.optimizer.performance_model import (
    PerformanceCost,
    PerformanceEstimate,
)
from src.optimizer.performance_plan import (
    OptimizationCandidate,
)


def main():
    source = PerformanceEstimate(
        name="lth-baseline",
        cost=PerformanceCost(
            time=200,
            memory=160,
            states=180,
            branching=120,
            depth=90,
            precision=100,
            interactions=140,
        ),
        meaning_signature="lth-core-v1",
    )

    candidate = OptimizationCandidate(
        name="lth-optimized",
        cost=PerformanceCost(
            time=100,
            memory=120,
            states=100,
            branching=90,
            depth=80,
            precision=100,
            interactions=100,
        ),
        meaning_signature="lth-core-v1",
        semantics_preserved=True,
    )

    result = LeatherPerformanceEngine().optimize(
        source=source,
        candidates=(candidate,),
        function=lambda: {"price": 135.45},
        optimized_function=lambda: {"price": 135.45},
    )

    assert result.valid
    assert result.evidence.output_equal
    assert result.sea_certificate.valid

    print("LEATHER PERFORMANCE REGRESSION: PASS")


if __name__ == "__main__":
    main()
