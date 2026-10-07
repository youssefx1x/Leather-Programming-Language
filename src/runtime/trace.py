from dataclasses import dataclass, field


@dataclass(frozen=True)
class TraceEvent:
    kind: str
    message: str
    data: dict = field(default_factory=dict)


class ExecutionTrace:
    def __init__(self):
        self.events = []

    def record(self, kind, message, **data):
        self.events.append(
            TraceEvent(
                kind=kind,
                message=message,
                data=data,
            )
        )

    def describe(self):
        lines = ["EXECUTION TRACE"]

        for event in self.events:
            lines.append(
                f"  {event.kind}: {event.message}"
            )

        return "\n".join(lines)
