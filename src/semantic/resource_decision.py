from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceDecision:
    resource: str
    value: object
    reason: str


class ResourceDecisionEngine:
    """
    Convert resource constraints into planner-level decisions.
    """

    def decide(self, envelope):
        decisions = []

        if envelope.memory_mb is not None:
            if envelope.memory_mb < 512:
                decisions.append(
                    ResourceDecision(
                        "memory.strategy",
                        "streaming",
                        "low memory envelope favors streaming execution",
                    )
                )
            elif envelope.memory_mb < 1024:
                decisions.append(
                    ResourceDecision(
                        "memory.strategy",
                        "bounded",
                        "moderate memory envelope favors bounded memory usage",
                    )
                )
            else:
                decisions.append(
                    ResourceDecision(
                        "memory.strategy",
                        "adaptive",
                        "larger memory envelope allows adaptive execution",
                    )
                )

        if envelope.time_ms is not None:
            if envelope.time_ms < 1000:
                decisions.append(
                    ResourceDecision(
                        "execution.mode",
                        "latency",
                        "tight time envelope favors latency-oriented execution",
                    )
                )
            else:
                decisions.append(
                    ResourceDecision(
                        "execution.mode",
                        "balanced",
                        "time envelope allows balanced execution",
                    )
                )

        if envelope.gpu is not None and envelope.gpu > 0:
            decisions.append(
                ResourceDecision(
                    "compute.target",
                    "gpu",
                    "GPU resource is available in the envelope",
                )
            )

        return decisions
