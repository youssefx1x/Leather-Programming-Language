from src.runtime.adaptive import AdaptiveRuntime
from src.runtime.observation import RuntimeObservation
from src.runtime.morphing import PlanMorpher
from src.runtime.morphing_evidence import MorphingEvidence


class MorphingRuntime(AdaptiveRuntime):
    """
    Adaptive runtime capable of changing execution strategy
    when runtime observations justify a different strategy.
    """

    def __init__(self):
        super().__init__()

        self.morpher = PlanMorpher()
        self.morphing_evidence = MorphingEvidence()
        self.active_strategies = {}

    def execute(self, ir, context=None):
        result = super().execute(
            ir,
            context=context,
        )

        self.active_strategies = {}

        execution_strategies = {
            "latency",
            "balanced",
            "streaming",
            "adaptive",
        }

        for strategy in self.strategies:
            if strategy.name not in execution_strategies:
                continue

            self.active_strategies[
                strategy.target_name
            ] = strategy.name

        return result

    def observe_and_morph(
        self,
        target,
        observation,
    ):
        current = self.active_strategies.get(target)

        if current is None:
            return None

        decision = self.morpher.decide(
            target=target,
            current_strategy=current,
            observation=observation,
        )

        if decision is None:
            return None

        self.active_strategies[target] = (
            decision.new_strategy
        )

        self.morphing_evidence.record(
            target=decision.target,
            old_strategy=decision.old_strategy,
            new_strategy=decision.new_strategy,
            reason=decision.reason,
        )

        self.adaptive_evidence.record(
            target,
            decision.new_strategy,
            "plan-morphed",
            decision.reason,
        )

        return decision

    def strategy_for(self, target_name):
        return self.active_strategies.get(target_name)
