from dataclasses import dataclass
from time import perf_counter_ns


@dataclass(frozen=True)
class SEAEvaluationResult:
    value: object
    generated: int
    expanded: int
    unique_states: int
    cache_hits: int
    elapsed_ns: int

    @property
    def seconds(self):
        return self.elapsed_ns / 1_000_000_000


@dataclass(frozen=True)
class SEAOptimizationComparison:
    baseline: SEAEvaluationResult
    optimized: SEAEvaluationResult
    output_equal: bool

    @property
    def generated_reduction(self):
        if self.baseline.generated == 0:
            return 0.0

        return 1.0 - (
            self.optimized.generated
            / self.baseline.generated
        )

    @property
    def expansion_reduction(self):
        if self.baseline.expanded == 0:
            return 0.0

        return 1.0 - (
            self.optimized.expanded
            / self.baseline.expanded
        )

    @property
    def valid(self):
        return self.output_equal

    def summary(self):
        return {
            "output_equal": self.output_equal,
            "generated_reduction": self.generated_reduction,
            "expansion_reduction": self.expansion_reduction,
            "baseline_generated": self.baseline.generated,
            "optimized_generated": self.optimized.generated,
            "cache_hits": self.optimized.cache_hits,
        }


class SEANaiveEvaluator:
    def __init__(self, key_fn=None):
        self.key_fn = key_fn or (lambda state: state)

    def evaluate(
        self,
        start,
        expand,
        terminal,
        combine,
        max_depth=128,
    ):
        started = perf_counter_ns()

        generated = 0
        expanded = 0

        def visit(state, depth):
            nonlocal generated
            nonlocal expanded

            generated += 1

            if depth > max_depth:
                raise ValueError(
                    "maximum evaluation depth exceeded"
                )

            if terminal(state):
                return combine(
                    state,
                    (),
                )

            expanded += 1

            children = tuple(
                expand(state)
            )

            values = tuple(
                visit(child, depth + 1)
                for child in children
            )

            return combine(
                state,
                values,
            )

        value = visit(start, 0)

        elapsed = perf_counter_ns() - started

        return SEAEvaluationResult(
            value=value,
            generated=generated,
            expanded=expanded,
            unique_states=generated,
            cache_hits=0,
            elapsed_ns=elapsed,
        )


class SEAMemoizedEvaluator:
    def __init__(self, key_fn=None):
        self.key_fn = key_fn or (lambda state: state)

    def evaluate(
        self,
        start,
        expand,
        terminal,
        combine,
        max_depth=128,
    ):
        started = perf_counter_ns()

        generated = 0
        expanded = 0
        cache_hits = 0

        cache = {}
        active = set()

        def visit(state, depth):
            nonlocal generated
            nonlocal expanded
            nonlocal cache_hits

            generated += 1

            if depth > max_depth:
                raise ValueError(
                    "maximum evaluation depth exceeded"
                )

            key = self.key_fn(state)

            if key in cache:
                cache_hits += 1
                return cache[key]

            if key in active:
                raise ValueError(
                    "cycle detected during memoized evaluation"
                )

            active.add(key)

            try:
                if terminal(state):
                    result = combine(
                        state,
                        (),
                    )
                else:
                    expanded += 1

                    children = tuple(
                        expand(state)
                    )

                    values = tuple(
                        visit(child, depth + 1)
                        for child in children
                    )

                    result = combine(
                        state,
                        values,
                    )

                cache[key] = result
                return result

            finally:
                active.remove(key)

        value = visit(start, 0)

        elapsed = perf_counter_ns() - started

        return SEAEvaluationResult(
            value=value,
            generated=generated,
            expanded=expanded,
            unique_states=len(cache),
            cache_hits=cache_hits,
            elapsed_ns=elapsed,
        )


def compare_evaluation(
    start,
    expand,
    terminal,
    combine,
    key_fn=None,
    max_depth=128,
):
    baseline = SEANaiveEvaluator(
        key_fn=key_fn
    ).evaluate(
        start=start,
        expand=expand,
        terminal=terminal,
        combine=combine,
        max_depth=max_depth,
    )

    optimized = SEAMemoizedEvaluator(
        key_fn=key_fn
    ).evaluate(
        start=start,
        expand=expand,
        terminal=terminal,
        combine=combine,
        max_depth=max_depth,
    )

    return SEAOptimizationComparison(
        baseline=baseline,
        optimized=optimized,
        output_equal=(
            baseline.value
            == optimized.value
        ),
    )
