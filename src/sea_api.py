from src.sea_engine import SEAEngine
from src.sea_engine04 import SEA04Engine
from src.sea_memo import compare_evaluation
from src.sea_equivalence import SEAEquivalenceRelation


class SEA:
    """
    Unified public interface for SEA 1.0 Foundation.
    """

    VERSION = "1.0-foundation"

    def __init__(self):
        self.arithmetic = SEAEngine()
        self.computation = SEA04Engine()

    def version(self):
        return self.VERSION

    def evaluate(self, operation, left, right):
        return self.arithmetic.evaluate(
            operation,
            left,
            right,
        )

    def search(self, domain, max_depth=16):
        return self.computation.search(
            domain,
            max_depth=max_depth,
        )

    def graph(self, domain, max_depth=8):
        return self.computation.build_graph(
            domain,
            max_depth=max_depth,
        )

    def equivalent(self, values, key_fn):
        return SEAEquivalenceRelation(
            key_fn
        ).partition(values)

    def optimize(
        self,
        start,
        expand,
        terminal,
        combine,
        key_fn=None,
        max_depth=128,
    ):
        return compare_evaluation(
            start=start,
            expand=expand,
            terminal=terminal,
            combine=combine,
            key_fn=key_fn,
            max_depth=max_depth,
        )
