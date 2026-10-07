from src.execution.result_cache import ResultCache


def main():
    cache = ResultCache(capacity=2)

    cache.set(
        {"state": 1},
        "A",
    )

    assert cache.get(
        {"state": 1}
    ) == "A"

    cache.set(
        {"state": 2},
        "B",
    )

    cache.set(
        {"state": 3},
        "C",
    )

    assert cache.size() == 2
    assert not cache.contains(
        {"state": 1}
    )

    stats = cache.stats()

    assert stats["capacity"] == 2
    assert stats["hits"] >= 1

    print("LTH RESULT CACHE: PASS")


if __name__ == "__main__":
    main()
