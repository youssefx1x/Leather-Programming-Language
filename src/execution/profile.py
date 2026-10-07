from dataclasses import dataclass

from src.optimizer.performance_model import PerformanceCost


@dataclass(frozen=True)
class ExecutionProfile:
    estimated: PerformanceCost
    observed: PerformanceCost

    @property
    def time_ratio(self):
        if self.estimated.time == 0:
            return 1.0
        return self.observed.time / self.estimated.time

    @property
    def memory_ratio(self):
        if self.estimated.memory == 0:
            return 1.0
        return self.observed.memory / self.estimated.memory

    @property
    def state_ratio(self):
        if self.estimated.states == 0:
            return 1.0
        return self.observed.states / self.estimated.states

    def within_factor(self, factor=10.0):
        return all(
            1.0 / factor <= ratio <= factor
            for ratio in (
                self.time_ratio,
                self.memory_ratio,
                self.state_ratio,
            )
        )

    def summary(self):
        return {
            "estimated": self.estimated.render(),
            "observed": self.observed.render(),
            "time_ratio": self.time_ratio,
            "memory_ratio": self.memory_ratio,
            "state_ratio": self.state_ratio,
            "within_factor": self.within_factor(),
        }
