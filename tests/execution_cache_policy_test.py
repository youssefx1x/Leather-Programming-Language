from src.execution.cache_policy import CachePolicy


def main():
    policy = CachePolicy()

    disabled = policy.decide(
        repeated_subproblems=0.0,
        states=100,
    )

    enabled = policy.decide(
        repeated_subproblems=0.70,
        states=100,
        memory_budget=1000,
    )

    pressured = policy.decide(
        repeated_subproblems=0.70,
        states=2000,
        memory_budget=1000,
    )

    assert not disabled.enabled
    assert enabled.enabled
    assert not pressured.enabled

    print("LTH CACHE POLICY: PASS")


if __name__ == "__main__":
    main()
