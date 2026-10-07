from src.runtime.unified import UnifiedRuntime
from src.runtime.morphic_registry import MorphicRegistry
from src.runtime.strategy import RuntimeStrategyResolver
from src.runtime.adaptive_evidence import RuntimeAdaptiveEvidence


class AdaptiveRuntime(UnifiedRuntime):
    """
    Runtime layer that understands optimization strategies
    while preserving the existing LTH runtime behavior.
    """

    def __init__(self):
        super().__init__()

        self.morphic = MorphicRegistry()
        self.strategy_resolver = (
            RuntimeStrategyResolver()
        )

        self.adaptive_evidence = (
            RuntimeAdaptiveEvidence()
        )

        self.strategies = []

    def execute(
        self,
        ir,
        context=None,
    ):
        self.strategies = (
            self.strategy_resolver.resolve(ir)
        )

        self._prepare_strategies()

        result = super().execute(
            ir,
            context=context,
        )

        self._capture_values()

        return result

    def _prepare_strategies(self):
        for strategy in self.strategies:
            self.adaptive_evidence.record(
                strategy.target_name,
                strategy.name,
                "strategy-selected",
                strategy.reason,
            )

    def _capture_values(self):
        for name, value in self.state.values.items():
            if isinstance(value, bool):
                semantic_type = "boolean"
            elif isinstance(value, (int, float)):
                semantic_type = "number"
            elif isinstance(value, str):
                semantic_type = "string"
            else:
                semantic_type = "dynamic"

            existing = self.morphic.get(name)

            if existing is None:
                self.morphic.define(
                    name,
                    semantic_type,
                    value,
                )
            else:
                existing.value = value

    def strategy_for(self, target_name):
        return [
            strategy
            for strategy in self.strategies
            if strategy.target_name == target_name
        ]
