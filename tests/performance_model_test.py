from src.optimizer.performance_model import (
    PerformanceCost,
    PerformanceEstimate,
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
        time=60,
        memory=80,
        states=55,
        branching=70,
        depth=90,
        precision=100,
        interactions=65,
    )

    assert target.dominates(source)
    assert not source.dominates(target)

    estimate = PerformanceEstimate(
        name="baseline",
        cost=source,
        meaning_signature="price-flow-v1",
    )

    assert estimate.describe()["name"] == "baseline"
    assert source.total() == 700

    print("LTH PERFORMANCE MODEL: PASS")


if __name__ == "__main__":
    main()
