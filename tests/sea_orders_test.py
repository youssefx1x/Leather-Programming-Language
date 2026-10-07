from src.sea_orders import (
    SEADominance,
    SEAMetricVector,
    SEAParetoFrontier,
    SEAParetoPoint,
    pareto_compare,
)


def main():
    assert pareto_compare(
        (1, 2),
        (2, 3),
    ) == SEADominance.BETTER

    assert pareto_compare(
        (2, 3),
        (1, 2),
    ) == SEADominance.WORSE

    assert pareto_compare(
        (1, 2),
        (1, 2),
    ) == SEADominance.EQUAL

    assert pareto_compare(
        (1, 5),
        (5, 1),
    ) == SEADominance.INCOMPARABLE

    frontier = SEAParetoFrontier(
        points=(
            SEAParetoPoint(
                "A",
                SEAMetricVector((1, 5)),
            ),
            SEAParetoPoint(
                "B",
                SEAMetricVector((5, 1)),
            ),
            SEAParetoPoint(
                "C",
                SEAMetricVector((4, 4)),
            ),
            SEAParetoPoint(
                "D",
                SEAMetricVector((7, 7)),
            ),
        )
    )

    names = {
        point.name
        for point in frontier.nondominated()
    }

    assert names == {"A", "B", "C"}

    print(
        "SEA 0.3 PARETO COMPLEXITY: PASS"
    )


if __name__ == "__main__":
    main()
