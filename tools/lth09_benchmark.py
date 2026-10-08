from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.lth09.engine import AcceleratedEngine


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tests/lth09/lth09_benchmark.json"


def baseline(values):
    total = 0
    for left, right in values:
        total += left + right
    return total


def accelerated(values):
    engine = AcceleratedEngine()
    total = 0

    for left, right in values:
        total += engine.add(left, right)

    return total, engine.stats


def measure(function, repeats=7):
    samples = []

    result = None

    for _ in range(repeats):
        start = time.perf_counter_ns()
        result = function()
        samples.append(time.perf_counter_ns() - start)

    return result, {
        "min_ns": min(samples),
        "median_ns": statistics.median(samples),
        "mean_ns": statistics.mean(samples),
    }


def main():
    # Repeated workload deliberately exposes a real memoization opportunity.
    values = [
        (2.5, 0.5),
        (10.0, 5.0),
        (2.5, 0.5),
        (10.0, 5.0),
    ] * 25000

    baseline_result, baseline_time = measure(
        lambda: baseline(values)
    )

    accelerated_result, stats = measure(
        lambda: accelerated(values)
    )

    accelerated_value, accelerated_stats = accelerated_result

    if baseline_result != accelerated_value:
        raise SystemExit(
            f"semantic mismatch: {baseline_result} != {accelerated_value}"
        )

    if accelerated_stats.cache_hits <= 0:
        raise SystemExit("expected cache hits were not observed")

    baseline_ns = baseline_time["median_ns"]

    # Re-measure accelerated execution separately so the reported metric
    # compares equivalent benchmark functions.
    _, accelerated_time = measure(
        lambda: accelerated(values)
    )

    accelerated_ns = accelerated_time["median_ns"]

    speedup = (
        baseline_ns / accelerated_ns
        if accelerated_ns > 0
        else 0.0
    )

    payload = {
        "workload": {
            "pairs": len(values),
            "repetition_factor": 25000,
            "semantic_result": baseline_result,
        },
        "baseline": baseline_time,
        "accelerated": accelerated_time,
        "speedup_x": speedup,
        "acceleration": {
            "fast_path_hits": accelerated_stats.fast_path_hits,
            "cache_hits": accelerated_stats.cache_hits,
            "cache_misses": accelerated_stats.cache_misses,
        },
    }

    OUT.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )

    print("LTH 0.9 BENCHMARK: PASS")
    print(f"WORKLOAD PAIRS: {len(values)}")
    print(f"SEMANTIC RESULT: {baseline_result}")
    print(f"BASELINE MEDIAN NS: {baseline_ns}")
    print(f"ACCELERATED MEDIAN NS: {accelerated_ns}")
    print(f"SPEEDUP X: {speedup:.3f}")
    print(f"CACHE HITS: {accelerated_stats.cache_hits}")
    print(f"FAST PATH HITS: {accelerated_stats.fast_path_hits}")

    if speedup <= 1.0:
        print("PERFORMANCE GAIN: NOT ESTABLISHED")
    else:
        print("PERFORMANCE GAIN: ESTABLISHED")


if __name__ == "__main__":
    main()
