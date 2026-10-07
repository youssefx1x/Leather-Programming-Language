from src.sea_memo import compare_evaluation


def main():
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

    result = compare_evaluation(
        start=12,
        expand=expand,
        terminal=terminal,
        combine=combine,
        key_fn=lambda state: state,
        max_depth=13,
    )

    assert result.valid
    assert result.baseline.value == result.optimized.value
    assert result.optimized.cache_hits > 0
    assert result.optimized.generated < result.baseline.generated

    print("SEA 1.0 MEMOIZED OPTIMIZATION: PASS")


if __name__ == "__main__":
    main()
