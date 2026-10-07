from dataclasses import dataclass

from src.sea_memo import compare_evaluation
from src.sea_engine04 import SEA04Engine, demo_grid_domain


@dataclass(frozen=True)
class SEAFinalBenchmark:
    recurrence_n: int
    baseline_value: object
    optimized_value: object
    baseline_generated: int
    optimized_generated: int
    generated_reduction: float
    cache_hits: int
    search_generated_reduction: float

    @property
    def valid(self):
        return (
            self.baseline_value
            == self.optimized_value
        )


def run_recursive_benchmark(n=18):
    def expand(state):
        if state <= 1:
            return ()

        return (
            state - 1,
            state - 2,
        )

    def terminal(state):
        return state <= 1

    def combine(state, children):
        if terminal(state):
            return 1

        return sum(children)

    comparison = compare_evaluation(
        start=n,
        expand=expand,
        terminal=terminal,
        combine=combine,
        key_fn=lambda state: state,
        max_depth=n + 1,
    )

    searcher = SEA04Engine()

    search_report = searcher.search(
        demo_grid_domain(4),
        max_depth=6,
    )

    return SEAFinalBenchmark(
        recurrence_n=n,
        baseline_value=comparison.baseline.value,
        optimized_value=comparison.optimized.value,
        baseline_generated=comparison.baseline.generated,
        optimized_generated=comparison.optimized.generated,
        generated_reduction=
            comparison.generated_reduction,
        cache_hits=
            comparison.optimized.cache_hits,
        search_generated_reduction=
            search_report.generated_reduction,
    )


def render_benchmark(benchmark):
    return {
        "recurrence_n":
            benchmark.recurrence_n,
        "value":
            benchmark.optimized_value,
        "baseline_generated":
            benchmark.baseline_generated,
        "optimized_generated":
            benchmark.optimized_generated,
        "generated_reduction":
            benchmark.generated_reduction,
        "cache_hits":
            benchmark.cache_hits,
        "search_generated_reduction":
            benchmark.search_generated_reduction,
        "valid":
            benchmark.valid,
    }
