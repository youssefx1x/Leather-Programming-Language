from src.sea_search import (
    SEASearchSpace,
    SEASearchProfile,
)


def main():
    space = SEASearchSpace(
        branching=2,
        depth=10,
    )

    assert space.frontier() == 1024
    assert space.total_nodes() == 2047

    profile = SEASearchProfile(
        name="binary_search_tree",
        search_space=space,
        node_cost=2.0,
    )

    assert profile.estimated_work() == 4094.0

    summary = profile.summary()

    assert summary["total_nodes"] == 2047

    symbolic = SEASearchSpace(
        branching=2,
        depth=12,
    )

    huge = symbolic.huge_total_nodes()

    assert huge.scientific_exponent == 3
    assert huge.scientific_mantissa > 2

    print(
        "SEA 0.2 SEARCH SPACE MODEL: PASS"
    )


if __name__ == "__main__":
    main()
