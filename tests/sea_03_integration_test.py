from src.sea_complexity import ComplexityExpr
from src.sea_factorial import SEAFactorial
from src.sea_orders import (
    SEAMetricVector,
    SEAParetoFrontier,
    SEAParetoPoint,
)
from src.sea_space_algebra import (
    SEAStateSpaceAlgebra,
)
from src.sea_symbolic import normalize


def main():
    n = ComplexityExpr.symbol("n")

    raw = (
        (n * n)
        + (0 * n)
    )

    simplified = normalize(raw)

    assert simplified.evaluate(
        {"n": 20}
    ) == 400

    state_space = (
        SEAStateSpaceAlgebra(
            dimensions=(8, 8, 8, 8)
        )
    )

    assert (
        state_space.total_states()
        == 4096
    )

    factorial = SEAFactorial(100)

    assert factorial.digits() == 158

    frontier = SEAParetoFrontier(
        points=(
            SEAParetoPoint(
                "raw",
                SEAMetricVector(
                    (1000, 1000, 1000)
                ),
            ),
            SEAParetoPoint(
                "memory_saver",
                SEAMetricVector(
                    (500, 1000, 1500)
                ),
            ),
            SEAParetoPoint(
                "balanced",
                SEAMetricVector(
                    (700, 700, 700)
                ),
            ),
        )
    )

    names = {
        point.name
        for point in frontier.nondominated()
    }

    assert "balanced" in names
    assert "raw" not in names

    print(
        "SEA 0.3 FULL MATHEMATICAL INTEGRATION: PASS"
    )


if __name__ == "__main__":
    main()
