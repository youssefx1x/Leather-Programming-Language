from src.semantic.unified_intent import UnifiedIntentContext
from src.semantic.resource_decision import ResourceDecisionEngine


class ResourceIntentResolver:
    """
    Resolve ResourceEnvelope constraints into UnifiedIntentContext decisions.
    """

    def __init__(self, decision_engine=None):
        self.decision_engine = (
            decision_engine or ResourceDecisionEngine()
        )

    def resolve(self, envelope):
        intent = UnifiedIntentContext()

        decisions = self.decision_engine.decide(envelope)

        for decision in decisions:
            intent.set_decision(
                decision.resource,
                decision.value,
                decision.reason,
            )

        return intent
