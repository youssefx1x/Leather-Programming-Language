from dataclasses import dataclass
from enum import Enum

from src.optimizer.performance_model import PerformanceCost


class WorkloadKind(Enum):
    DIRECT = "direct"
    SEARCH = "search"
    TREE = "tree"
    GRAPH = "graph"
    ITERATIVE = "iterative"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ExecutionWorkload:
    name: str
    kind: WorkloadKind = WorkloadKind.UNKNOWN
    states: int = 1
    branching: int = 1
    depth: int = 1
    repeated_subproblems: float = 0.0
    interactions: int = 1
    precision: int = 1
    memory_budget: int | None = None

    def __post_init__(self):
        if self.states < 1:
            raise ValueError("states must be >= 1")
        if self.branching < 1:
            raise ValueError("branching must be >= 1")
        if self.depth < 1:
            raise ValueError("depth must be >= 1")
        if not 0.0 <= self.repeated_subproblems <= 1.0:
            raise ValueError("repeated_subproblems must be in [0, 1]")

    @property
    def estimated_work(self):
        return self.states * self.branching

    def base_cost(self):
        return PerformanceCost(
            time=float(self.estimated_work),
            memory=float(self.states),
            states=float(self.states),
            branching=float(self.branching),
            depth=float(self.depth),
            precision=float(self.precision),
            interactions=float(self.interactions),
        )

    def strategy_cost(self, strategy):
        base = self.base_cost()

        if strategy == "direct":
            return base

        if strategy == "memoized":
            reuse = max(0.10, self.repeated_subproblems)
            return PerformanceCost(
                time=max(1.0, base.time * (1.0 - 0.75 * reuse)),
                memory=base.memory * (1.0 + 0.15 * reuse),
                states=max(1.0, base.states * (1.0 - 0.70 * reuse)),
                branching=base.branching,
                depth=base.depth,
                precision=base.precision,
                interactions=base.interactions,
            )

        if strategy == "shared_state":
            return PerformanceCost(
                time=max(1.0, base.time * 0.70),
                memory=max(1.0, base.memory * 0.80),
                states=max(1.0, base.states * 0.55),
                branching=max(1.0, base.branching * 0.85),
                depth=base.depth,
                precision=base.precision,
                interactions=max(1.0, base.interactions * 0.75),
            )

        if strategy == "streaming":
            return PerformanceCost(
                time=base.time * 1.05,
                memory=max(1.0, base.memory * 0.25),
                states=base.states,
                branching=base.branching,
                depth=base.depth,
                precision=base.precision,
                interactions=base.interactions,
            )

        return base
