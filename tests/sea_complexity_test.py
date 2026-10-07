from src.sea_complexity import (
    ComplexityExpr,
    SEAComplexity,
)


def main():
    n = ComplexityExpr.symbol("n")

    linear = n
    quadratic = n ** 2
    exponential = 2 ** n

    assert linear.evaluate({"n": 8}) == 8
    assert quadratic.evaluate({"n": 8}) == 64
    assert exponential.evaluate({"n": 8}) == 256

    first = SEAComplexity(
        time=10,
        memory=20,
        states=100,
        branching=4,
        depth=5,
        precision=1,
        interactions=7,
    )

    second = SEAComplexity(
        time=2,
        memory=10,
        states=50,
        branching=2,
        depth=2,
        precision=1,
        interactions=3,
    )

    assert second.dominates_numeric(first)

    combined = first.sequential(second)

    assert combined.time.numeric_value() == 12
    assert combined.depth.numeric_value() == 7
    assert combined.memory.numeric_value() == 20
    assert combined.states.numeric_value() == 100
    assert combined.branching.numeric_value() == 4
    assert combined.interactions.numeric_value() == 10

    symbolic = SEAComplexity(
        time=2 ** n,
        memory=n,
        states=n ** 2,
        branching=2,
        depth=n,
        precision=1,
        interactions=n,
    )

    assert symbolic.numeric_tuple() is None

    print("SEA 0.1 COMPLEXITY ALGEBRA: PASS")


if __name__ == "__main__":
    main()
