from src.sea_complexity import SEAComplexity
from src.sea_laws import SEAComplexityLawSet


def main():
    a = SEAComplexity(
        time=10,
        memory=20,
        states=100,
        branching=4,
        depth=5,
        precision=2,
        interactions=7,
    )

    b = SEAComplexity(
        time=20,
        memory=30,
        states=200,
        branching=6,
        depth=8,
        precision=3,
        interactions=9,
    )

    laws = SEAComplexityLawSet()

    sequential = laws.sequential(a, b)

    assert sequential.time.numeric_value() == 30
    assert sequential.memory.numeric_value() == 30
    assert sequential.depth.numeric_value() == 13
    assert sequential.interactions.numeric_value() == 16

    parallel = laws.parallel(a, b)

    assert parallel.time.numeric_value() == 20
    assert parallel.memory.numeric_value() == 50
    assert parallel.states.numeric_value() == 300
    assert parallel.depth.numeric_value() == 8

    search = laws.search(2, 10)

    assert search.frontier_nodes() == 1024
    assert search.total_nodes() == 2047

    print(
        "SEA 0.2 COMPLEXITY LAWS: PASS"
    )


if __name__ == "__main__":
    main()
