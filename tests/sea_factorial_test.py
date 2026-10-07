from src.sea_factorial import SEAFactorial


def main():
    small = SEAFactorial(10)

    assert small.exact() == 3628800
    assert small.digits() == 7

    large = SEAFactorial(1000)

    assert large.digits() == 2568

    exact_log = large.log10()
    approximation = large.stirling_log10()

    assert exact_log > 250
    assert abs(
        exact_log - approximation
    ) < 0.001

    huge = large.huge()

    assert (
        huge.scientific_exponent
        == 2567
    )

    print(
        "SEA 0.3 FACTORIAL SCALE: PASS"
    )


if __name__ == "__main__":
    main()
