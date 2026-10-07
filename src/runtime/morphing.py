from dataclasses import dataclass


@dataclass(frozen=True)
class MorphDecision:
    target: str
    old_strategy: str
    new_strategy: str
    reason: str


class PlanMorpher:
    """
    Changes execution strategy without changing semantic intent.
    """

    def decide(self, target, current_strategy, observation):
        if (
            current_strategy == "latency"
            and observation.memory_mb is not None
            and observation.memory_mb < 256
        ):
            return MorphDecision(
                target=target,
                old_strategy=current_strategy,
                new_strategy="streaming",
                reason="memory pressure requires streaming execution",
            )

        if (
            current_strategy == "balanced"
            and observation.elapsed_ms is not None
            and observation.elapsed_ms > 1000
        ):
            return MorphDecision(
                target=target,
                old_strategy=current_strategy,
                new_strategy="latency",
                reason="observed latency exceeded balanced target",
            )

        if (
            current_strategy == "streaming"
            and observation.memory_mb is not None
            and observation.memory_mb >= 1024
        ):
            return MorphDecision(
                target=target,
                old_strategy=current_strategy,
                new_strategy="adaptive",
                reason="memory availability permits adaptive execution",
            )

        return None
