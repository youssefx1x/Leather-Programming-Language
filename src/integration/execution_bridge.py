from dataclasses import dataclass

from src.execution.cost import observed_cost
from src.execution.profile import ExecutionProfile
from src.integration.sea_bridge import LEATHERSEABridge


@dataclass(frozen=True)
class ExecutionSEAView:
    source_cost: object
    optimized_cost: object
    source_sea: object
    optimized_sea: object

    @property
    def improved(self):
        return self.optimized_cost.dominates(
            self.source_cost
        )


class ExecutionSEABridge:
    @staticmethod
    def compare(
        source_measurement,
        optimized_measurement,
    ):
        source_cost = observed_cost(
            source_measurement
        )

        optimized_cost = observed_cost(
            optimized_measurement
        )

        return ExecutionSEAView(
            source_cost=source_cost,
            optimized_cost=optimized_cost,
            source_sea=LEATHERSEABridge.to_sea(
                source_cost
            ),
            optimized_sea=LEATHERSEABridge.to_sea(
                optimized_cost
            ),
        )

    @staticmethod
    def profile(
        estimated,
        measurement,
    ):
        return ExecutionProfile(
            estimated=estimated,
            observed=observed_cost(
                measurement
            ),
        )

    @staticmethod
    def certificate(view, name):
        return LEATHERSEABridge.certificate(
            name=name,
            source_cost=view.source_cost,
            target_cost=view.optimized_cost,
            semantics_preserved=True,
        )
