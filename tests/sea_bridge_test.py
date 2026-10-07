from src.integration.sea_bridge import (
    LEATHERSEABridge,
)
from src.optimizer.performance_model import (
    PerformanceCost,
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

    sea = LEATHERSEABridge.to_sea(source)
    restored = LEATHERSEABridge.from_sea(sea)

    assert restored == source

    certificate = LEATHERSEABridge.certificate(
        name="test-optimization",
        source_cost=source,
        target_cost=target,
        semantics_preserved=True,
    )

    assert certificate.valid
    assert certificate.summary()["valid"]

    print("LTH ↔ SEA BRIDGE: PASS")


if __name__ == "__main__":
    main()
