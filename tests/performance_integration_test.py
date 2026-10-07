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
        name="baseline-search",
        cost=PerformanceCost(
            time=100,
            memory=100,
            states=100,
            branching=100,
            depth=100,
            precision=100,
            interactions=100,
        ),
        meaning_signature="search-domain-v1",
    )

    candidate = OptimizationCandidate(
        name="shared-state-search",
        cost=PerformanceCost(
            time=40,
            memory=75,
            states=45,
            branching=70,
            depth=90,
            precision=100,
            interactions=60,
        ),
        meaning_signature="search-domain-v1",
        semantics_preserved=True,
        rationale="share equivalent computational states",
    )

    def baseline():
        return 55

    def optimized():
        return 55

    result = LeatherPerformanceEngine().optimize(
        source=source,
        candidates=(candidate,),
        function=baseline,
        optimized_function=optimized,
    )

    assert result.plan.valid
    assert result.sea_certificate.valid
    assert result.evidence.valid
    assert result.valid

    print("LTH PERFORMANCE + SEA INTEGRATION: PASS")


if __name__ == "__main__":
    main()
