from src.sea_api import SEA
from src.sea_engine04 import demo_grid_domain


def main():
    sea = SEA()

    assert sea.version() == "1.0-foundation"

    value = sea.evaluate(
        "multiply",
        6,
        7,
    )

    assert value.is_regular
    assert value.value == 42

    graph = sea.graph(
        demo_grid_domain(3),
        max_depth=4,
    )

    assert graph.stats().nodes > 0

    print("SEA 1.0 PUBLIC API: PASS")


if __name__ == "__main__":
    main()
