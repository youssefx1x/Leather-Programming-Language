from dataclasses import dataclass

from src.optimizer.performance_model import PerformanceCost


@dataclass(frozen=True)
class ExecutionBudget:
    max_time: float | None = None
    max_memory: float | None = None
    max_states: float | None = None
    max_operations: float | None = None
    max_depth: float | None = None

    def fits(self, cost: PerformanceCost):
        limits = (
            ("time", cost.time, self.max_time),
            ("memory", cost.memory, self.max_memory),
            ("states", cost.states, self.max_states),
            ("operations", cost.interactions, self.max_operations),
            ("depth", cost.depth, self.max_depth),
        )

        return all(
            limit is None or value <= limit
            for _, value, limit in limits
        )

    def violations(self, cost: PerformanceCost):
        violations = []

        checks = (
            ("time", cost.time, self.max_time),
            ("memory", cost.memory, self.max_memory),
            ("states", cost.states, self.max_states),
            ("operations", cost.interactions, self.max_operations),
            ("depth", cost.depth, self.max_depth),
        )

        for name, value, limit in checks:
            if limit is not None and value > limit:
                violations.append(
                    {
                        "dimension": name,
                        "value": value,
                        "limit": limit,
                    }
                )

        return tuple(violations)

    def describe(self):
        return {
            "max_time": self.max_time,
            "max_memory": self.max_memory,
            "max_states": self.max_states,
            "max_operations": self.max_operations,
            "max_depth": self.max_depth,
        }
