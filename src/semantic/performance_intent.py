from dataclasses import dataclass


@dataclass(frozen=True)
class PerformanceIntent:
    target: str = "balanced"
    preserve_semantics: bool = True
    maximize_throughput: bool = True
    minimize_memory: bool = False
    assumptions: tuple = ()

    def describe(self):
        return {
            "target": self.target,
            "preserve_semantics":
                self.preserve_semantics,
            "maximize_throughput":
                self.maximize_throughput,
            "minimize_memory":
                self.minimize_memory,
            "assumptions": self.assumptions,
        }
