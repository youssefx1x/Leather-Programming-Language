from dataclasses import dataclass


@dataclass(frozen=True)
class CacheDecision:
    enabled: bool
    reason: str
    expected_reuse: float
    memory_pressure: float

    def describe(self):
        return {
            "enabled": self.enabled,
            "reason": self.reason,
            "expected_reuse": self.expected_reuse,
            "memory_pressure": self.memory_pressure,
        }


class CachePolicy:
    def decide(
        self,
        repeated_subproblems,
        states,
        memory_budget=None,
    ):
        if repeated_subproblems <= 0.0:
            return CacheDecision(
                enabled=False,
                reason="no repeated subproblem signal",
                expected_reuse=0.0,
                memory_pressure=0.0,
            )

        pressure = (
            0.0
            if memory_budget is None
            else states / max(1, memory_budget)
        )

        if pressure > 1.0:
            return CacheDecision(
                enabled=False,
                reason="memory pressure too high",
                expected_reuse=repeated_subproblems,
                memory_pressure=pressure,
            )

        if repeated_subproblems < 0.10:
            return CacheDecision(
                enabled=False,
                reason="reuse signal too weak",
                expected_reuse=repeated_subproblems,
                memory_pressure=pressure,
            )

        return CacheDecision(
            enabled=True,
            reason="repeated subproblems justify caching",
            expected_reuse=repeated_subproblems,
            memory_pressure=pressure,
        )
