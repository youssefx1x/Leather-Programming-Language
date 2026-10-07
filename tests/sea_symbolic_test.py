from src.sea_complexity import ComplexityExpr
from src.sea_symbolic import normalize


def main():
    n = ComplexityExpr.symbol("n")

    zero = ComplexityExpr.const(0)
    one = ComplexityExpr.const(1)

    assert normalize(
        n + zero
    ).simplified == n

    assert normalize(
        n * one
    ).simplified == n

    assert normalize(
        n + n
    ).simplified == 2 * n

    assert normalize(
        n * n
    ).simplified == n ** 2

    assert normalize(
        n ** 1
    ).simplified == n

    assert normalize(
        n ** 0
    ).simplified.evaluate({}) == 1

    result = normalize(
        (n * n) + 0
    )

    assert result.evaluate(
        {"n": 7}
    ) == 49

    print(
        "SEA 0.3 SYMBOLIC NORMALIZATION: PASS"
    )


if __name__ == "__main__":
    main()
