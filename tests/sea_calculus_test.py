from src.sea_calculus import (
    linear,
    quadratic,
    cubic,
    exponential,
    logarithmic,
    sqrt,
    compare_growth,
)


def main():
    l = linear()
    q = quadratic()
    c = cubic()
    e = exponential()
    log = logarithmic()
    root = sqrt()

    assert l.evaluate(10) == 10
    assert q.evaluate(10) == 100
    assert c.evaluate(10) == 1000
    assert e.evaluate(10) == 1024

    assert root.evaluate(100) == 10
    assert log.evaluate(1) == 0

    result = compare_growth(
        l,
        q,
        points=(10, 100),
    )

    assert result["relation"] == "slower_growth"

    result = compare_growth(
        q,
        l,
        points=(10, 100),
    )

    assert result["relation"] == "faster_growth"

    same = compare_growth(
        l,
        linear(),
        points=(10, 100),
    )

    assert same["relation"] == "equivalent"

    print("SEA 0.1 COMPLEXITY CALCULUS: PASS")


if __name__ == "__main__":
    main()
