from dataclasses import dataclass
from enum import Enum


class ExecutionStrategy(Enum):
    DIRECT = "direct"
    MEMOIZED = "memoized"
    SHARED_STATE = "shared_state"
    STREAMING = "streaming"
    ADAPTIVE = "adaptive"


@dataclass(frozen=True)
class ExecutionDecision:
    strategy: ExecutionStrategy
    reason: str
    confidence: float

    def describe(self):
        return {
            "strategy": self.strategy.value,
            "reason": self.reason,
            "confidence": self.confidence,
        }
