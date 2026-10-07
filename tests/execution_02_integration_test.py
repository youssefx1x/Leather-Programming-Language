from src.execution.benchmark import (
    ExecutionBenchmark,
)
from src.execution.budget import ExecutionBudget
from src.execution.cache_policy import (
    CachePolicy,
)
from src.execution.controller import (
    AdaptiveExecutionController,
)
from src.execution.model import (
    ExecutionWorkload,
    WorkloadKind,
)
from src.execution.result_cache import (
    ResultCache,
)
from src.execution.scheduler import (
    ExecutionScheduler,
)
from src.execution.search_workload import (
    fibonacci_direct,
    fibonacci_memoized,
)
from src.semantic.adaptive_performance import (
    AdaptivePerformanceIntent,
)
from src.semantic.execution_intent import (
    ExecutionIntent,
)


def main():
    workload = ExecutionWorkload(
        name="sea-aware-search",
        kind=WorkloadKind.TREE,
        states=400,
        branching=2,
        depth=21,
        repeated_subproblems=0.85,
        memory_budget=1000,
    )

    cache_decision = CachePolicy().decide(
        repeated_subproblems=workload.repeated_subproblems,
        states=workload.states,
        memory_budget=workload.memory_budget,
    )

    assert cache_decision.enabled

    cache = ResultCache(capacity=8)

    cache.set(
        ("fib", 10),
        55,
    )

    assert cache.get(
        ("fib", 10)
    ) == 55

    batches = ExecutionScheduler().partition(
        range(20),
        batch_size=5,
    )

    assert len(batches) == 4

    intent = ExecutionIntent(
        target="adaptive",
        preserve_semantics=True,
        allow_memoization=True,
        allow_shared_state=True,
        allow_streaming=True,
        require_measured_evidence=True,
    )

    result = AdaptiveExecutionController().run(
        workload=workload,
        source_function=lambda c:
            fibonacci_direct(21, c),
        optimized_function=lambda c:
            fibonacci_memoized(21, c),
        intent=intent,
        budget=ExecutionBudget(
            max_memory=1000,
            max_states=400,
            max_depth=30,
        ),
    )

    assert result.plan.valid
    assert result.benchmark.output_equal
    assert result.benchmark.operations_saved > 0
    assert result.sea_certificate.valid
    assert result.valid

    adaptive_intent = AdaptivePerformanceIntent(
        objective="state-efficient-search",
        preserve_semantics=True,
        prefer_time=True,
        prefer_memory=False,
        prefer_state_reduction=True,
        require_evidence=True,
    )

    assert adaptive_intent.weights()["states"] > 1.0

    benchmark = ExecutionBenchmark().compare(
        source_function=lambda c:
            fibonacci_direct(17, c),
        optimized_function=lambda c:
            fibonacci_memoized(17, c),
    )

    assert benchmark.valid

    print("LEATHER EXECUTION 0.2 INTEGRATION: PASS")


if __name__ == "__main__":
    main()
