from dataclasses import dataclass, field


@dataclass(frozen=True)
class OptimizationEvidence:
    step_name: str
    strategy: str
    reason: str
    source: str


@dataclass
class OptimizationEvidenceLog:
    events: list = field(default_factory=list)

    def record(self, step_name, strategy, reason, source):
        event = OptimizationEvidence(
            step_name=step_name,
            strategy=strategy,
            reason=reason,
            source=source,
        )

        self.events.append(event)
        return event

    def find(self, step_name=None, strategy=None):
        results = self.events

        if step_name is not None:
            results = [
                event for event in results
                if event.step_name == step_name
            ]

        if strategy is not None:
            results = [
                event for event in results
                if event.strategy == strategy
            ]

        return results

    def why(self, step_name):
        return [
            event
            for event in self.events
            if event.step_name == step_name
        ]

    def describe(self):
        lines = ["OPTIMIZATION EVIDENCE"]

        for event in self.events:
            lines.append(
                f"  {event.step_name}: {event.strategy}"
            )
            lines.append(
                f"    reason = {event.reason}"
            )
            lines.append(
                f"    source = {event.source}"
            )

        return "\n".join(lines)
