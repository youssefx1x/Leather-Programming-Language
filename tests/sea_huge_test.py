from src.sea_huge import SEAHugeNumber


def main():
    huge = SEAHugeNumber.power(
        2,
        1000,
    )

    assert huge.decimal_digits == 302
    assert huge.scientific_exponent == 301

    larger = SEAHugeNumber.power(
        2,
        2000,
    )

    assert larger.compare(huge) == 1

    assert (
        huge.scientific_mantissa > 1
        and huge.scientific_mantissa < 10
    )

    rendered = huge.render()

    assert rendered.startswith("1.0715")
    assert "e301" in rendered

    print("SEA 0.1 HUGE NUMBER MODEL: PASS")


if __name__ == "__main__":
    main()
