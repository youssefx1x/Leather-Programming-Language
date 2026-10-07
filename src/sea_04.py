from dataclasses import dataclass

from src.sea_engine04 import SEA04Engine, demo_grid_domain
from src.sea_recurrence import (
    binary_tree_recurrence,
    fibonacci_recurrence,
)


@dataclass(frozen=True)
class SEA04Report:
    recurrence: dict
    search: dict
    graph: dict
    equivalence: dict

    @property
    def valid(self):
        return (
            self.search["valid"]
            and self.graph["valid"]
            and self.equivalence["class_count"]
            <= self.equivalence["original_count"]
        )


def build_demo_report():
    engine = SEA04Engine()

    fib = fibonacci_recurrence()
    recurrence = {
        "fib_10": fib.evaluate(10),
        "fib_20": fib.evaluate(20),
    }

    tree = binary_tree_recurrence()

    search_report = engine.search(
        demo_grid_domain(4),
        max_depth=6,
    )

    graph = engine.build_graph(
        demo_grid_domain(4),
        max_depth=6,
    )

    equivalence_values = (
        (1, 2),
        (2, 1),
        (1, 2),
        (3, 0),
        (0, 3),
    )

    equivalence = engine.equivalence(
        equivalence_values,
        key_fn=lambda value: tuple(sorted(value)),
    )

    return SEA04Report(
        recurrence={
            **recurrence,
            "binary_tree_8": tree.evaluate(8),
        },
        search={
            "valid": search_report.tree_valid
            and search_report.graph_valid,
            "generated_reduction":
                search_report.generated_reduction,
            "tree_generated":
                search_report.comparison.tree.generated,
            "graph_generated":
                search_report.comparison.graph.generated,
        },
        graph={
            "valid": engine.validate_graph(graph).valid,
            "nodes": graph.stats().nodes,
            "edges": graph.stats().edges,
            "acyclic": graph.stats().acyclic,
        },
        equivalence={
            "original_count": equivalence.original_count,
            "class_count": equivalence.class_count,
            "compression_ratio":
                equivalence.compression_ratio,
        },
    )
