from src.sea_metrics import (
    SEAMetrics,
    SEAComparisonMetrics,
)


def main():
    baseline = SEAMetrics(
        generated=100,
        expanded=90,
        unique_states=80,
        elapsed_ns=1000,
    )

    optimized = SEAMetrics(
        generated=40,
        expanded=30,
        unique_states=35,
        elapsed_ns=700,
    )

    comparison = SEAComparisonMetrics(
        baseline=baseline,
        optimized=optimized,
    )

    assert baseline.duplicate_count == 20
    assert baseline.compression_ratio == 1.25
    assert comparison.generated_reduction == 0.6
    assert comparison.state_reduction == 0.5625

    print("SEA 0.4 METRICS: PASS")


if __name__ == "__main__":
    main()
