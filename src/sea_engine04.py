from dataclasses import dataclass

from src.sea_domain import SEADomain
from src.sea_equivalence import SEAEquivalenceRelation
from src.sea_graph import SEAGraph
from src.sea_graph_search import (
    SEAGraphSearch,
    SEASearchComparison,
)
from src.sea_validation import (
    validate_graph,
    validate_search_result,
)


@dataclass(frozen=True)
class SEA04SearchReport:
    domain: str
    comparison: SEASearchComparison
    tree_valid: bool
    graph_valid: bool

    @property
    def equivalent_result(self):
        return self.comparison.valid

    @property
    def generated_reduction(self):
        return self.comparison.generated_reduction


class SEA04Engine:
    """
    SEA 0.4 computational integration layer.

    Combines:
      - explicit state equivalence
      - graph representation
      - bounded search
      - validation
      - measurable compression
    """

    def __init__(self):
        pass

    def build_graph(self, domain, max_depth=8):
        graph = SEAGraph(key_fn=domain.key)

        frontier = [(domain.initial, 0)]
        seen = {domain.key(domain.initial)}

        while frontier:
            state, depth = frontier.pop(0)
            graph.add_node(state)

            if depth >= max_depth:
                continue

            for child in domain.expand(state):
                graph.add_edge(state, child)
                key = domain.key(child)

                if key not in seen:
                    seen.add(key)
                    frontier.append((child, depth + 1))

        return graph

    def search(self, domain, max_depth=16):
        searcher = SEAGraphSearch(
            key_fn=domain.key
        )

        tree = searcher.search(
            start=domain.initial,
            goal=domain.goal,
            expand=domain.expand,
            max_depth=max_depth,
            mode="tree",
        )

        graph = searcher.search(
            start=domain.initial,
            goal=domain.goal,
            expand=domain.expand,
            max_depth=max_depth,
            mode="graph",
        )

        comparison = SEASearchComparison(
            tree=tree,
            graph=graph,
        )

        return SEA04SearchReport(
            domain=domain.name,
            comparison=comparison,
            tree_valid=validate_search_result(tree).valid,
            graph_valid=validate_search_result(graph).valid,
        )

    def equivalence(self, values, key_fn):
        relation = SEAEquivalenceRelation(key_fn)
        return relation.partition(values)

    def validate_graph(self, graph):
        return validate_graph(graph)


def demo_grid_domain(size=4):
    target = (size - 1, size - 1)

    def expand(state):
        x, y = state

        candidates = (
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        )

        return tuple(
            child
            for child in candidates
            if 0 <= child[0] < size
            and 0 <= child[1] < size
        )

    return SEADomain(
        name=f"grid_{size}x{size}",
        initial=(0, 0),
        expand=expand,
        goal=lambda state: state == target,
        key_fn=lambda state: state,
        metadata=(
            ("type", "finite_grid"),
            ("size", size),
        ),
    )
