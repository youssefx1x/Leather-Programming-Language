from collections import deque
from dataclasses import dataclass
from time import perf_counter_ns


@dataclass(frozen=True)
class SEASearchResult:
    found: bool
    path: tuple
    depth: int
    generated: int
    expanded: int
    unique_states: int
    duplicate_pruned: int
    elapsed_ns: int
    mode: str

    @property
    def seconds(self):
        return self.elapsed_ns / 1_000_000_000

    @property
    def compression_ratio(self):
        if self.unique_states == 0:
            return 1.0

        return self.generated / self.unique_states


class SEAGraphSearch:
    """
    Deterministic BFS over finite or bounded state spaces.

    graph mode:
        exact state deduplication / transposition-style pruning.

    tree mode:
        no global deduplication, useful for measuring expansion redundancy.
    """

    def __init__(self, key_fn=None):
        self.key_fn = key_fn or (lambda state: state)

    def search(
        self,
        start,
        goal,
        expand,
        max_depth=32,
        mode="graph",
    ):
        if mode not in ("graph", "tree"):
            raise ValueError("mode must be 'graph' or 'tree'")

        started = perf_counter_ns()

        queue = deque()
        queue.append((start, 0, (start,)))

        visited = set()

        if mode == "graph":
            visited.add(self.key_fn(start))

        generated = 1
        expanded = 0
        duplicate_pruned = 0

        while queue:
            state, depth, path = queue.popleft()
            expanded += 1

            if goal(state):
                elapsed = perf_counter_ns() - started

                return SEASearchResult(
                    found=True,
                    path=path,
                    depth=depth,
                    generated=generated,
                    expanded=expanded,
                    unique_states=(
                        len(visited)
                        if mode == "graph"
                        else generated
                    ),
                    duplicate_pruned=duplicate_pruned,
                    elapsed_ns=elapsed,
                    mode=mode,
                )

            if depth >= max_depth:
                continue

            for child in expand(state):
                generated += 1
                child_key = self.key_fn(child)

                if mode == "graph":
                    if child_key in visited:
                        duplicate_pruned += 1
                        continue

                    visited.add(child_key)

                queue.append(
                    (
                        child,
                        depth + 1,
                        path + (child,),
                    )
                )

        elapsed = perf_counter_ns() - started

        return SEASearchResult(
            found=False,
            path=(),
            depth=-1,
            generated=generated,
            expanded=expanded,
            unique_states=(
                len(visited)
                if mode == "graph"
                else generated
            ),
            duplicate_pruned=duplicate_pruned,
            elapsed_ns=elapsed,
            mode=mode,
        )


@dataclass(frozen=True)
class SEASearchComparison:
    tree: SEASearchResult
    graph: SEASearchResult

    @property
    def generated_reduction(self):
        if self.tree.generated == 0:
            return 0.0

        return 1.0 - (
            self.graph.generated / self.tree.generated
        )

    @property
    def expansion_reduction(self):
        if self.tree.expanded == 0:
            return 0.0

        return 1.0 - (
            self.graph.expanded / self.tree.expanded
        )

    @property
    def valid(self):
        return self.tree.found == self.graph.found


def compare_search(
    start,
    goal,
    expand,
    key_fn=None,
    max_depth=32,
):
    searcher = SEAGraphSearch(key_fn=key_fn)

    tree = searcher.search(
        start=start,
        goal=goal,
        expand=expand,
        max_depth=max_depth,
        mode="tree",
    )

    graph = searcher.search(
        start=start,
        goal=goal,
        expand=expand,
        max_depth=max_depth,
        mode="graph",
    )

    return SEASearchComparison(
        tree=tree,
        graph=graph,
    )
