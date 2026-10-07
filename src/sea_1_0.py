from dataclasses import dataclass

from src.sea_api import SEA
from src.sea_certificates import (
    SEACondition,
    certify_optimization,
)
from src.sea_final_benchmark import (
    render_benchmark,
    run_recursive_benchmark,
)
from src.sea_engine04 import demo_grid_domain


@dataclass(frozen=True)
class SEA10Report:
    version: str
    arithmetic_ok: bool
    graph_ok: bool
    optimization_ok: bool
    benchmark_ok: bool
    certificate_ok: bool

    @property
    def valid(self):
        return all(
            (
                self.arithmetic_ok,
                self.graph_ok,
                self.optimization_ok,
                self.benchmark_ok,
                self.certificate_ok,
            )
        )


def build_final_report():
    sea = SEA()

    arithmetic = sea.evaluate(
        "add",
        10,
        20,
    )

    domain = demo_grid_domain(4)

    graph = sea.graph(
        domain,
        max_depth=6,
    )

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

    optimization = sea.optimize(
        start=12,
        expand=expand,
        terminal=terminal,
        combine=combine,
        key_fn=lambda state: state,
        max_depth=13,
    )

    benchmark = run_recursive_benchmark(
        n=18,
    )

    certificate = certify_optimization(
        name="SEA-OPT-FIB-DAG",
        source_result=optimization.baseline.value,
        target_result=optimization.optimized.value,
        semantic_equivalence=optimization.output_equal,
        conditions=(
            SEACondition(
                "same_output",
                optimization.output_equal,
            ),
            SEACondition(
                "unique_state_cache",
                optimization.optimized.unique_states
                <= optimization.baseline.generated,
            ),
            SEACondition(
                "measured_reduction",
                optimization.generated_reduction >= 0.0,
            ),
        ),
    )

    return SEA10Report(
        version=sea.version(),
        arithmetic_ok=(
            arithmetic.is_regular
            and arithmetic.value == 30
        ),
        graph_ok=(
            graph.stats().nodes > 0
            and graph.stats().edges > 0
        ),
        optimization_ok=(
            optimization.valid
            and optimization.generated_reduction > 0.0
        ),
        benchmark_ok=(
            benchmark.valid
            and benchmark.optimized_generated
            <= benchmark.baseline_generated
        ),
        certificate_ok=certificate.valid,
    )


def main():
    report = build_final_report()

    assert report.valid

    benchmark = run_recursive_benchmark(
        n=18,
    )

    print("SEA 1.0 FINAL FOUNDATION: PASS")
    print("VERSION:", report.version)
    print(
        "RECURSIVE BASELINE NODES:",
        benchmark.baseline_generated,
    )
    print(
        "RECURSIVE OPTIMIZED NODES:",
        benchmark.optimized_generated,
    )
    print(
        "GENERATED REDUCTION:",
        benchmark.generated_reduction,
    )
    print(
        "CACHE HITS:",
        benchmark.cache_hits,
    )
    print(
        "SEARCH REDUCTION:",
        benchmark.search_generated_reduction,
    )


if __name__ == "__main__":
    main()
