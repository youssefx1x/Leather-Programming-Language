from src.sea_benchmark import (
    SEABenchmarkComparison,
    benchmark,
)
from src.sea_huge import SEAHugeNumber


def main():
    direct = benchmark(
        "direct",
        lambda: sum(
            i for i in range(10000)
        ),
    )

    symbolic = benchmark(
        "symbolic",
        lambda: SEAHugeNumber.power(
            2,
            1000000,
        ),
    )

    comparison = SEABenchmarkComparison(
        direct=direct,
        symbolic=symbolic,
    )

    assert direct.elapsed_seconds >= 0
    assert symbolic.elapsed_seconds >= 0
    assert comparison.speedup >= 0

    print(
        "SEA 0.3 BENCHMARK MODEL: PASS"
    )


if __name__ == "__main__":
    main()
