from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionIntent:
    target: str = "adaptive"
    preserve_semantics: bool = True
    allow_memoization: bool = True
    allow_shared_state: bool = True
    allow_streaming: bool = True
    require_measured_evidence: bool = True

    def permits(self, strategy):
        allowed = {
            "memoized": self.allow_memoization,
            "shared_state": self.allow_shared_state,
            "streaming": self.allow_streaming,
            "direct": True,
            "adaptive": True,
        }

        return allowed.get(strategy, False)

    def describe(self):
        return {
            "target": self.target,
            "preserve_semantics":
                self.preserve_semantics,
            "allow_memoization":
                self.allow_memoization,
            "allow_shared_state":
                self.allow_shared_state,
            "allow_streaming":
                self.allow_streaming,
            "require_measured_evidence":
                self.require_measured_evidence,
        }
