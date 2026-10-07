from src.optimizer.performance_model import (
    PerformanceCost,
)
from src.runtime.performance_evidence import (
    PerformanceEvidence,
)


def main():
    source = PerformanceCost(
        time=100,
        memory=100,
        states=100,
        branching=100,
        depth=100,
        precision=100,
        interactions=100,
    )

    target = PerformanceCost(
        time=50,
        memory=70,
        states=60,
        branching=80,
        depth=90,
        precision=100,
        interactions=65,
    )

    evidence = PerformanceEvidence(
        name="memoized",
        source_output=55,
        target_output=55,
        source_cost=source,
        target_cost=target,
        semantics_preserved=True,
    )

    assert evidence.output_equal
    assert evidence.resource_improved
    assert evidence.valid

    print("LTH PERFORMANCE EVIDENCE: PASS")


if __name__ == "__main__":
    main()
