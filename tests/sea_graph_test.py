from src.sea_graph import SEAGraph
from src.sea_validation import validate_graph


def main():
    graph = SEAGraph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    assert len(graph.nodes()) == 4
    assert len(graph.edges()) == 3
    assert graph.is_acyclic()
    assert graph.topological_order()[0] == "A"

    reachable = graph.reachable_from("A")
    assert len(reachable) == 4

    report = validate_graph(graph)
    assert report.valid

    print("SEA 0.4 GRAPH/DAG MODEL: PASS")


if __name__ == "__main__":
    main()
