import time

from src.lth03.final_runner import LTH03FinalRunner

from .runner import LTH04Runner


def benchmark(
    source,
    context=None,
    iterations=10,
):
    reference = LTH03FinalRunner()
    accelerated = LTH04Runner(
        use_cache=True
    )

    reference.run(
        source,
        context=context,
    )

    accelerated.run(
        source,
        context=context,
    )

    start = time.perf_counter()

    for _ in range(iterations):
        reference.run(
            source,
            context=context,
        )

    reference_total = (
        time.perf_counter() - start
    )

    start = time.perf_counter()

    for _ in range(iterations):
        accelerated.run(
            source,
            context=context,
        )

    accelerated_total = (
        time.perf_counter() - start
    )

    reference_avg = (
        reference_total / iterations
    )

    accelerated_avg = (
        accelerated_total / iterations
    )

    ratio = (
        reference_avg / accelerated_avg
        if accelerated_avg > 0
        else 0.0
    )

    return {
        "iterations": iterations,
        "reference_total": reference_total,
        "accelerated_total": accelerated_total,
        "reference_avg": reference_avg,
        "accelerated_avg": accelerated_avg,
        "speedup_ratio": ratio,
    }
