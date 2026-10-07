from src.runtime.performance_runtime import (
    PerformanceRuntime,
)


def main():
    runtime = PerformanceRuntime()

    measurement = runtime.measure(
        lambda: sum(range(100))
    )

    assert measurement.result == 4950
    assert measurement.elapsed_ns >= 0
    assert measurement.seconds >= 0.0

    print("LTH PERFORMANCE RUNTIME: PASS")


if __name__ == "__main__":
    main()
