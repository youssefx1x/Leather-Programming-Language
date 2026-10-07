from src.sea_bounds import (
    SEABound,
    validate_bound,
)
from src.sea_complexity import ComplexityExpr
from src.sea_growth import SEAAsymptoticKind


def main():
    n = ComplexityExpr.symbol("n")
    f = n ** 2

    upper = SEABound(
        kind=SEAAsymptoticKind.O,
        function=f,
        bound=2 * f,
    )

    lower = SEABound(
        kind=SEAAsymptoticKind.OMEGA,
        function=f,
        bound=f,
    )

    tight = SEABound(
        kind=SEAAsymptoticKind.THETA,
        function=f,
        bound=f,
    )

    assert validate_bound(
        upper
    ).validated

    assert validate_bound(
        lower
    ).validated

    assert validate_bound(
        tight
    ).validated

    print(
        "SEA 0.2 BOUNDS: PASS"
    )


if __name__ == "__main__":
    main()
