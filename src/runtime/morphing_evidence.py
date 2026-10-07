from dataclasses import dataclass, field


@dataclass(frozen=True)
class MorphingEvent:
    target: str
    old_strategy: str
    new_strategy: str
    reason: str


@dataclass
class MorphingEvidence:
    events: list = field(default_factory=list)

    def record(
        self,
        target,
        old_strategy,
        new_strategy,
        reason,
    ):
        event = MorphingEvent(
            target=target,
            old_strategy=old_strategy,
            new_strategy=new_strategy,
            reason=reason,
        )

        self.events.append(event)
        return event

    def find(self, target=None):
        if target is None:
            return list(self.events)

        return [
            event
            for event in self.events
            if event.target == target
        ]

    def describe(self):
        lines = ["PLAN MORPHING EVIDENCE"]

        for event in self.events:
            lines.append(
                f"  {event.target}: "
                f"{event.old_strategy} -> "
                f"{event.new_strategy}"
            )
            lines.append(
                f"    reason = {event.reason}"
            )

        return "\n".join(lines)
