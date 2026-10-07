from src.sea_complexity import SEAComplexity
from src.sea_profile import SEAComplexityProfile


def main():
    slow = SEAComplexityProfile(
        name="naive",
        complexity=SEAComplexity(
            time=1000,
            memory=500,
            states=10000,
            branching=10,
            depth=100,
            precision=4,
            interactions=500,
        ),
    )

    fast = SEAComplexityProfile(
        name="compressed",
        complexity=SEAComplexity(
            time=100,
            memory=300,
            states=1000,
            branching=5,
            depth=50,
            precision=4,
            interactions=100,
        ),
    )

    result = fast.compare(slow)

    assert result["this_dominates"] is True
    assert result["other_dominates"] is False

    summary = fast.summary()

    assert summary["name"] == "compressed"

    print("SEA 0.1 COMPLEXITY PROFILE: PASS")


if __name__ == "__main__":
    main()
