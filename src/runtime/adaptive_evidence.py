from dataclasses import dataclass, field


@dataclass(frozen=True)
class RuntimeAdaptiveEvent:
    target: str
    strategy: str
    action: str
    reason: str


@dataclass
class RuntimeAdaptiveEvidence:
    events: list = field(default_factory=list)

    def record(
        self,
        target,
        strategy,
        action,
        reason,
    ):
        event = RuntimeAdaptiveEvent(
            target=target,
            strategy=strategy,
            action=action,
            reason=reason,
        )

        self.events.append(event)
        return event

    def find(self, target=None, strategy=None):
        results = self.events

        if target is not None:
            results = [
                event
                for event in results
                if event.target == target
            ]

        if strategy is not None:
            results = [
                event
                for event in results
                if event.strategy == strategy
            ]

        return results

    def describe(self):
        lines = ["RUNTIME ADAPTIVE EVIDENCE"]

        for event in self.events:
            lines.append(
                f"  {event.target}: {event.strategy}"
            )
            lines.append(
                f"    action = {event.action}"
            )
            lines.append(
                f"    reason = {event.reason}"
            )

        return "\n".join(lines)
