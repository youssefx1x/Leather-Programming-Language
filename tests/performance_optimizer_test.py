from src.optimizer.performance_model import (
    PerformanceCost,
    PerformanceEstimate,
)
from src.optimizer.performance_optimizer import (
    PerformanceOptimizer,
)
from src.optimizer.performance_plan import (
    OptimizationCandidate,
)


def main():
    source_cost = PerformanceCost(
        time=100,
        memory=100,
        states=100,
        branching=100,
        depth=100,
        precision=100,
        interactions=100,
    )

    source = PerformanceEstimate(
        name="baseline",
        cost=source_cost,
        meaning_signature="search-v1",
    )

    weak = OptimizationCandidate(
        name="weak",
        cost=PerformanceCost(
            time=120,
            memory=90,
            states=100,
            branching=100,
            depth=100,
            precision=100,
            interactions=100,
        ),
        meaning_signature="search-v1",
    )

    strong = OptimizationCandidate(
        name="strong",
        cost=PerformanceCost(
            time=50,
            memory=70,
            states=60,
            branching=80,
            depth=90,
            precision=100,
            interactions=65,
        ),
        meaning_signature="search-v1",
    )

    wrong_meaning = OptimizationCandidate(
        name="wrong-meaning",
        cost=PerformanceCost(
            time=10,
            memory=10,
            states=10,
            branching=10,
            depth=10,
            precision=10,
            interactions=10,
        ),
        meaning_signature="different-program",
    )

    result = PerformanceOptimizer().optimize(
        source,
        (
            weak,
            strong,
            wrong_meaning,
        ),
    )

    assert result.selected.name == "strong"
    assert result.improved
    assert result.valid

    print("LTH PERFORMANCE OPTIMIZER: PASS")


if __name__ == "__main__":
    main()
