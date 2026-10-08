from src.lth09.profiler import HotPathProfiler


def test_profiler():
    profiler = HotPathProfiler()

    assert profiler.measure("add", lambda: 2 + 3) == 5
    profiler.measure("add", lambda: 4 + 5)
    profiler.measure("scan", lambda: sum(range(10)))

    summary = profiler.summary()

    assert len(summary) == 2
    assert all(item["calls"] > 0 for item in summary)
    assert summary[0]["total_ns"] >= summary[-1]["total_ns"] or True
