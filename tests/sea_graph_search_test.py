from src.sea_graph_search import compare_search
from src.sea_engine04 import demo_grid_domain


def main():
    domain = demo_grid_domain(4)

    comparison = compare_search(
        start=domain.initial,
        goal=domain.goal,
        expand=domain.expand,
        key_fn=domain.key,
        max_depth=6,
    )

    assert comparison.valid
    assert comparison.tree.found
    assert comparison.graph.found
    assert comparison.graph.duplicate_pruned > 0
    assert comparison.graph.generated <= comparison.tree.generated

    print("SEA 0.4 SEARCH COMPRESSION: PASS")


if __name__ == "__main__":
    main()
