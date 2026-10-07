from src.semantic.unified_planner_builder import UnifiedSemanticPlanner
from src.semantic.unified_intent import UnifiedIntentContext


class IntentAwareUnifiedPlanner:
    """
    Unified planner with an explicit intent/decision layer.

    Intent affects execution strategy, not program meaning.
    """

    def __init__(self, decision_engine=None):
        self.base_planner = UnifiedSemanticPlanner()
        self.decision_engine = decision_engine

    def plan(self, semantic_program, intent=None):
        intent = intent or UnifiedIntentContext()

        plan = self.base_planner.plan(semantic_program)

        self._apply_intent(plan, intent)

        return plan

    def _apply_intent(self, plan, intent):
        for step in plan.steps:
            if step.kind == "FLOW":
                execution_mode = intent.get_decision(
                    "execution.mode"
                )

                if execution_mode:
                    step.details["execution_mode"] = (
                        execution_mode["value"]
                    )

            if step.kind == "DEFINE":
                strategy = intent.get_decision(
                    "memory.strategy"
                )

                if strategy:
                    step.details["memory_strategy"] = (
                        strategy["value"]
                    )


# Backward-compatible public name for existing integrations.
UnifiedIntentPlanner = IntentAwareUnifiedPlanner
