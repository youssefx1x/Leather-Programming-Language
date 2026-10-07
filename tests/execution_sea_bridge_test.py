from src.execution.cost import observed_cost
from src.execution.counter import ExecutionCounter
from src.execution.measurement import ExecutionMeasurer
from src.execution.search_workload import (
    fibonacci_direct,
    fibonacci_memoized,
)
from src.integration.execution_bridge import (
    ExecutionSEABridge,
)


def main():
    measurer = ExecutionMeasurer()

    a_counter = ExecutionCounter()
    b_counter = ExecutionCounter()

    a = measurer.measure(
        lambda c: fibonacci_direct(16, c),
        a_counter,
    )

    b = measurer.measure(
        lambda c: fibonacci_memoized(16, c),
        b_counter,
    )

    view = ExecutionSEABridge.compare(a, b)

    assert a.result == b.result
    assert view.improved

    profile = ExecutionSEABridge.profile(
        observed_cost(a),
        b,
    )

    assert profile.within_factor(100000.0)
    assert profile.summary()["observed"]["time"] > 0

    print("LTH EXECUTION ↔ SEA: PASS")


if __name__ == "__main__":
    main()
