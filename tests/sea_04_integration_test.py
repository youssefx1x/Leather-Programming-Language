from src.sea_04 import build_demo_report


def main():
    report = build_demo_report()

    assert report.valid

    assert report.recurrence["fib_10"] == 55
    assert report.recurrence["fib_20"] == 6765

    assert report.graph["valid"]
    assert report.graph["nodes"] > 0
    assert report.graph["edges"] > 0

    assert report.equivalence["class_count"] == 2
    assert report.equivalence["original_count"] == 5
    assert report.equivalence["compression_ratio"] == 2.5

    assert report.search["valid"]
    assert report.search["graph_generated"] <= \
        report.search["tree_generated"]

    print("SEA 0.4 FULL STRUCTURAL INTEGRATION: PASS")


if __name__ == "__main__":
    main()
