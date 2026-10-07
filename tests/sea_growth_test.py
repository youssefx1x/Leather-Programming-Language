from src.sea_growth import (
    SEAAsymptoticKind,
    SEAAsymptoticClaim,
    classify_growth,
    symbolic_growth_relation,
)
from src.sea_complexity import ComplexityExpr


def main():
    n = ComplexityExpr.symbol("n")

    linear = n
    quadratic = n ** 2
    exponential = 2 ** n
    logarithmic = ComplexityExpr(
        "log",
        (n,),
    )

    assert classify_growth(linear) == "linear"
    assert classify_growth(quadratic) == "quadratic"
    assert classify_growth(exponential) == "exponential"
    assert classify_growth(logarithmic) == "logarithmic"

    relation = symbolic_growth_relation(
        linear,
        exponential,
    )

    assert relation.relation == "slower_growth"
    assert relation.right_class == "exponential"

    claim = SEAAsymptoticClaim(
        kind=SEAAsymptoticKind.THETA,
        function=quadratic,
        reference=quadratic,
        statement=(
            "quadratic is Theta(quadratic)"
        ),
    )

    assert claim.render() == (
        "Theta((n ^ 2))"
    )

    print(
        "SEA 0.2 GROWTH ALGEBRA: PASS"
    )


if __name__ == "__main__":
    main()
