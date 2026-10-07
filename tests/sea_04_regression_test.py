from src.sea_04 import build_demo_report
from src.sea_complexity import SEAComplexity


def main():
    report = build_demo_report()

    assert report.valid

    complexity = SEAComplexity(
        time=report.search["tree_generated"],
        memory=report.search["graph_generated"],
        states=report.graph["nodes"],
        branching=4,
        depth=6,
        precision=1,
        interactions=report.graph["edges"],
    )

    assert complexity.numeric_tuple()[0] > 0
    assert complexity.numeric_tuple()[1] > 0
    assert complexity.numeric_tuple()[2] > 0

    print("SEA 0.4 CROSS-LAYER REGRESSION: PASS")


if __name__ == "__main__":
    main()
