from dataclasses import dataclass


@dataclass(frozen=True)
class SEAGraphStats:
    nodes: int
    edges: int
    reachable: int
    acyclic: bool


class SEAGraph:
    def __init__(self, key_fn=None):
        self.key_fn = key_fn or (lambda value: value)
        self._nodes = {}
        self._edges = {}

    def _key(self, value):
        return self.key_fn(value)

    def add_node(self, value):
        key = self._key(value)
        self._nodes.setdefault(key, value)
        self._edges.setdefault(key, set())
        return key

    def add_edge(self, source, target):
        source_key = self.add_node(source)
        target_key = self.add_node(target)
        self._edges[source_key].add(target_key)

    def has_node(self, value):
        return self._key(value) in self._nodes

    def nodes(self):
        return tuple(self._nodes.values())

    def edges(self):
        return tuple(
            (self._nodes[source], self._nodes[target])
            for source, targets in self._edges.items()
            for target in targets
        )

    def neighbors(self, value):
        key = self._key(value)
        return tuple(
            self._nodes[target]
            for target in self._edges.get(key, ())
        )

    def reachable_from(self, start):
        start_key = self._key(start)

        if start_key not in self._nodes:
            return ()

        visited = set()
        stack = [start_key]

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            for target in self._edges.get(current, ()):
                if target not in visited:
                    stack.append(target)

        return tuple(
            self._nodes[key]
            for key in visited
        )

    def is_acyclic(self):
        visiting = set()
        visited = set()

        def visit(node):
            if node in visiting:
                return False

            if node in visited:
                return True

            visiting.add(node)

            for target in self._edges.get(node, ()):
                if not visit(target):
                    return False

            visiting.remove(node)
            visited.add(node)
            return True

        return all(
            visit(node)
            for node in self._nodes
            if node not in visited
        )

    def topological_order(self):
        if not self.is_acyclic():
            raise ValueError("graph contains a cycle")

        indegree = {
            node: 0
            for node in self._nodes
        }

        for targets in self._edges.values():
            for target in targets:
                indegree[target] += 1

        queue = [
            node
            for node, degree in indegree.items()
            if degree == 0
        ]

        order = []

        while queue:
            node = queue.pop(0)
            order.append(self._nodes[node])

            for target in self._edges.get(node, ()):
                indegree[target] -= 1

                if indegree[target] == 0:
                    queue.append(target)

        return tuple(order)

    def stats(self, start=None):
        reachable = (
            len(self.reachable_from(start))
            if start is not None
            else len(self._nodes)
        )

        return SEAGraphStats(
            nodes=len(self._nodes),
            edges=sum(
                len(targets)
                for targets in self._edges.values()
            ),
            reachable=reachable,
            acyclic=self.is_acyclic(),
        )

    def quotient(self, key_fn):
        quotient = SEAGraph(key_fn=key_fn)

        for value in self.nodes():
            quotient.add_node(value)

        for source, target in self.edges():
            quotient.add_edge(source, target)

        return quotient
