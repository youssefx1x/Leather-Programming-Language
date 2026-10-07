from src.sea_final_benchmark import (
    run_recursive_benchmark,
)


def main():
    benchmark = run_recursive_benchmark(
        n=18,
    )

    assert benchmark.valid
    assert benchmark.baseline_generated > 0
    assert benchmark.optimized_generated > 0
    assert (
        benchmark.optimized_generated
        < benchmark.baseline_generated
    )
    assert benchmark.cache_hits > 0
    assert benchmark.generated_reduction > 0.0

    print("SEA 1.0 FINAL BENCHMARK: PASS")


if __name__ == "__main__":
    main()
