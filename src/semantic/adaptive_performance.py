from dataclasses import dataclass


@dataclass(frozen=True)
class AdaptivePerformanceIntent:
    objective: str = "balanced"
    preserve_semantics: bool = True
    prefer_time: bool = True
    prefer_memory: bool = False
    prefer_state_reduction: bool = True
    require_evidence: bool = True

    def weights(self):
        weights = {
            "time": 1.0,
            "memory": 0.50,
            "states": 0.75,
            "branching": 0.40,
            "depth": 0.20,
            "precision": 0.05,
            "interactions": 0.50,
        }

        if self.prefer_time:
            weights["time"] = 1.50

        if self.prefer_memory:
            weights["memory"] = 1.25

        if self.prefer_state_reduction:
            weights["states"] = 1.25

        return weights

    def describe(self):
        return {
            "objective": self.objective,
            "preserve_semantics":
                self.preserve_semantics,
            "weights": self.weights(),
            "require_evidence":
                self.require_evidence,
        }
