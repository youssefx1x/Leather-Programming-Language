from dataclasses import dataclass

from src.optimizer.performance_model import (
    PerformanceCost,
)
from src.sea_complexity import SEAComplexity
from src.sea_transform import (
    SEAOptimizationCertificate,
)


@dataclass(frozen=True)
class SEAOperationalView:
    performance_cost: PerformanceCost
    sea_complexity: SEAComplexity


class LEATHERSEABridge:
    """
    Bridge shared computational dimensions between
    Leather performance modeling and SEA complexity.
    """

    @staticmethod
    def to_sea(cost):
        return SEAComplexity(
            time=cost.time,
            memory=cost.memory,
            states=cost.states,
            branching=cost.branching,
            depth=cost.depth,
            precision=cost.precision,
            interactions=cost.interactions,
        )

    @staticmethod
    def from_sea(complexity):
        values = complexity.numeric_tuple()

        return PerformanceCost(
            time=values[0],
            memory=values[1],
            states=values[2],
            branching=values[3],
            depth=values[4],
            precision=values[5],
            interactions=values[6],
        )

    @classmethod
    def operational_view(cls, cost):
        return SEAOperationalView(
            performance_cost=cost,
            sea_complexity=cls.to_sea(cost),
        )

    @classmethod
    def certificate(
        cls,
        name,
        source_cost,
        target_cost,
        semantics_preserved=True,
        objective=None,
        allow_tradeoff=False,
    ):
        source = cls.to_sea(source_cost)
        target = cls.to_sea(target_cost)

        return SEAOptimizationCertificate(
            source_complexity=source,
            target_complexity=target,
            semantics_preserved=semantics_preserved,
            transformation_name=name,
            objective=objective,
            allow_tradeoff=allow_tradeoff,
        )
